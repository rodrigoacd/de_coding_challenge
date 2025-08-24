import sqlite3
import pandas
from flask import Flask, request, jsonify


# initialize the Flask application
app = Flask(__name__)


# get_db_connection() function is used to connect to the SQLite database
# and return a connection object
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn



############### API Endpoints                            ##########
################ First exercise                          ##########
################# The data is uploaded 1 table at a time ##########
@app.route('/upload_data', methods=['POST'])
def upload_data():
    '''
    Endpoint to upload CSV data to a specified table in the database.
    Expects a multipart/form-data request with:
    - 'file': The CSV file to upload.
    - 'table_name': The name of the table to which the data should be appended.
    
    Returns a JSON response indicating success or failure.
    '''
    # Check if the request contains a file and csv format
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    if not request.files['file'].filename.endswith('.csv'):
        return jsonify({"error": "File is not a CSV"}), 400
    
    # Get the file from the request
    file = request.files['file']
    
    # Get the table name from the request
    table_name = request.form.get('table_name')
    # Check the table name from the request
    if not table_name:
        return jsonify({"error": "Table name is required"}), 400
    

    # declare a dict with the table names and their columns like { table_name: [column1, column2, ...] }
    table_columns = {
        'hired_employees': ['id', 'name', 'datetime', 'department_id', 'job_id'],
        'departments': ['id', 'department_name'],
        'jobs': ['id', 'job_name'] }
    
    # 
    if table_name not in table_columns:
        return jsonify({"error": f"Table '{table_name}' does not exist"}), 400
    
    columns = table_columns[table_name]

    # Start processing the uploaded file
    try:
        conn = get_db_connection()
        # Read the CSV file into a pandas DataFrame
        df = pandas.read_csv(file, header=None, names=columns)
        
        # Ensure the table exists and append the file data
        df.to_sql(table_name, conn, if_exists='append', index=False)

        conn.close()

        return jsonify({"message": "Data uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



################ Second exercise   First endpoint          ##########
################# The data is retrieved in JSON format     ########## 
################# First I get the data from the database   ##########
################# Then I create the 2 endpoints that returns the data in JSON format and table ########## 
def employees_by_quarter_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH hired_plus_quarter AS(
        SELECT
            d.department_name, 
            j.job_name,
            CAST(strftime('%m', h.date) AS INT) AS month
            FROM hired_employees h 
            INNER JOIN jobs j 
                ON h.job_id = j.id 
            INNER JOIN departments d 
                ON d.id = h.department_id 
            WHERE strftime('%Y', h.date) = '2021' 
        )
        SELECT
            department_name, 
            job_name,
            SUM(CASE WHEN month BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1, 
            SUM(CASE WHEN month BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2, 
            SUM(CASE WHEN month BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3, 
            SUM(CASE WHEN month BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
        FROM hired_plus_quarter
        GROUP BY department_name, job_name
        ORDER BY department_name, job_name;
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results

# this returns the data as a JSON
@app.route('/employees_by_quarter', methods=['GET'])
def get_emp_by_dep_job():
    
    results = employees_by_quarter_data()
    # show results in a JSON format
    return jsonify([{
        "department_name": row[0],
        "job_name": row[1],
        "Q1": row[2],
        "Q2": row[3],
        "Q3": row[4],
        "Q4": row[5] } for row in results]), 200

# this returns the data as a table
@app.route('/employees_by_quarter_table', methods=['GET'])
def get_emp_by_dep_job_table():
    
    results = employees_by_quarter_data()

    # return results as a pandas DataFrame and convert it to HTML
    df = pandas.DataFrame(results, columns=['Department_name', 'Job_name', 'Q1', 'Q2', 'Q3', 'Q4'])
    # Convert DataFrame to HTML tablle
    return df.to_html(classes="table table-striped", index=False)


################# Second exercise   Second endpoint          ##########
################# The data is retrieved in JSON format and Table (to match with description)   ##########
def departments_above_mean_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        WITH hired_by_department AS (
            SELECT 
                d.id, 
                d.department_name, 
                count(*) AS count
            FROM hired_employees h 
            INNER JOIN departments d 
            ON h.department_id = d.id 
            WHERE strftime('%Y', h.date) = '2021'
            GROUP BY d.id, d.department_name ),
        mean_of_hired_by_department AS (
            SELECT 
                AVG(count) AS mean
            FROM hired_by_department
        )
        SELECT
            hbd.id,
            hbd.department_name,
            hbd.count
        FROM hired_by_department hbd
        WHERE hbd.count > (SELECT mean FROM mean_of_hired_by_department)
        ORDER BY hbd.count DESC;
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    return results


# this returns the data as a JSON
@app.route('/departments_above_mean', methods=['GET'])
def departments_above_mean():
    
    results = departments_above_mean_data()
    
    return jsonify([{
        "department_id": row[0],
        "department_name": row[1],
        "count": row[2]
    } for row in results]), 200

# this returns the data as a table
@app.route('/departments_above_mean_table', methods=['GET'])
def get_emp_by_dep_table():
    results = departments_above_mean_data()
    # return results as a pandas DataFrame and convert it to HTML
    df = pandas.DataFrame(results, columns=['department_id', 'department_name', 'count'])
    # Convert DataFrame to HTML tablle
    return df.to_html(classes="table table-striped", index=False)


################################
#### MAIN FUNCTION #############
if __name__ == '__main__':
    
    # Run the Flask application
    app.run(debug=True)

