import os
import pyodbc

def get_connection():
    base_conn_str = os.getenv("CONNECTION_STRING")
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"{base_conn_str}"
    )
    return pyodbc.connect(conn_str)
