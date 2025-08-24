# Flask SQLite Data Uploader

This project is a simple Flask API for uploading CSV data into an SQLite database. It supports uploading data to the `departments`, `hired_employees`, and `jobs` tables.

## Features

- REST API endpoint to upload CSV files to specific tables.
- SQLite database initialization with required tables.
- Error handling for missing files, table names, and invalid tables.

## Project Structure

```
app.py
database.db
departments.db
requirements.txt
upload/
    departments.csv
    hired_employees.csv
    jobs.csv
env/
    ...
```

## Requirements

- Python 3.10+
- Flask
- pandas

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

1. **Start the Flask server:**

    ```sh
    python app.py
    ```

2. **Upload data:**

    Send a POST request to `/upload_data` with:
    - A file (CSV format) as `file`
    - The target table name as `table_name` (must be one of: `departments`, `hired_employees`, `jobs`)

    Example using `curl`:

    ```sh
    curl -X POST -F "file=@upload/departments.csv" -F "table_name=departments" http://127.0.0.1:5000/upload_data
    ```

## API

### `POST /upload_data`

- **Parameters:**
    - `file`: CSV file to upload
    - `table_name`: Target table (`departments`, `hired_employees`, or `jobs`)

## Notes

- The database is initialized automatically when the server starts.
- Uploaded CSV files must match the table schema.

