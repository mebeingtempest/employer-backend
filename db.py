import os
import pyodbc

def get_connection():
    connection_string = os.getenv("CONNECTION_STRING")
    return pyodbc.connect(connection_string)
