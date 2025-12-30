import os
import pymssql

def get_connection():
    connection_string = os.getenv("CONNECTION_STRING")

    # Parse the connection string into a dictionary
    parts = dict(
        item.split('=', 1)
        for item in connection_string.split(';')
        if '=' in item
    )

    server = parts['Server'].replace('tcp:', '').split(',')[0]
    user = parts['Uid']
    password = parts['Pwd']
    database = parts['Database']

    return pymssql.connect(
        server=server,
        user=user,
        password=password,
        database=database
    )
