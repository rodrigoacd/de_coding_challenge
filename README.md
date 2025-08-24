# Data Engineer Challenge

## Overview
This project is a Flask application that allows users to upload CSV data into a SQLite database and retrieve various statistics about employees and departments.

## Installation

1. **Clone the repository**:

```bash
   git clone git@github.com:rodrigoacd/de_coding_challenge.git
   cd de_coding_challenge
```

2. **Set up a virtual environment** (optional but recommended):

```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the required packages**:
```bash
   pip install -r requirements.txt
```

## Running the Application

To run the Flask application, execute the following command:
```bash
gunicorn -w 4 -b 0.0.0.0:8000  app:app
``` 
The application will start on **http://0.0.0.0:8000**

## Endpoints 

### Section 1: API
#### Upload Data
- **Endpoint**: `/upload_data`
- **Method**: POST
- **Description**: Upload a CSV file to a specified table in the database.
- **Request Format**:
  - `file`: The CSV file to upload (must be in CSV format).
  - `table_name`: The name of the table to which the data should be appended.
- **Response**: JSON indicating success or failure.
- **Command**: 
```bash
curl -X POST http://0.0.0.0:8000/upload_data \
-F "file=@upload/hired_employees.csv" \
-F "table_name=hired_employees"

curl -X POST http://0.0.0.0:8000/upload_data \
-F "file=@upload/departments.csv" \
-F "table_name=departments"

curl -X POST http://0.0.0.0:8000/upload_data \
-F "file=@upload/jobs.csv" \
-F "table_name=jobs"

```

### Section 2: SQL

#### Get Employees by Quarter
- **Endpoint**: `/employees_by_quarter`
- **Method**: GET
- **Description**: Retrieve the number of hired employees by department and job for each quarter of 2021 in JSON format.
- **Response**: JSON array of objects containing department name, job name, and counts for each quarter.
- **Command**: 
```bash
curl -X GET http://0.0.0.0:8000/employees_by_quarter
```

#### Get Employees by Quarter (Table)
- **Endpoint**: `/employees_by_quarter_table`
- **Method**: GET
- **Description**: Retrieve the number of hired employees by department and job for each quarter of 2021 in HTML table format.
- **Response**: HTML table of the results.
- **Command**: 
``` bash
curl -X GET http://0.0.0.0:8000/employees_by_quarter_table
```
#### Departments Above Mean
- **Endpoint**: `/departments_above_mean`
- **Method**: GET
- **Description**: Retrieve departments that hired above the mean number of employees in 2021 in JSON format.
- **Response**: JSON array of objects containing department ID, name, and count.
- **Command**: 
``` bash
curl -X GET http://0.0.0.0:8000/departments_above_mean
```
#### Departments Above Mean (Table)
- **Endpoint**: `/departments_above_mean_table`
- **Method**: GET
- **Description**: Retrieve departments that hired above the mean number of employees in 2021 in HTML table format.
- **Response**: HTML table of the results.
- **Command**: 
``` bash
curl -X GET http://0.0.0.0:8000/departments_above_mean_table
```
## Conclusion
This project provides a simple API for managing employee data and statistics. You can extend it by adding more features or improving the data processing logic as needed.