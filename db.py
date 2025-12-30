import os
from sqlalchemy import create_engine

def get_connection():
    connection_string = os.getenv("CONNECTION_STRING")

    # Convert your Azure SQL connection string into a SQLAlchemy URL
    parts = dict(
        item.split('=', 1)
        for item in connection_string.split(';')
        if '=' in item
    )

    server = parts['Server'].replace('tcp:', '').split(',')[0]
    database = parts['Database']
    user = parts['Uid']
    password = parts['Pwd']

    # SQLAlchemy URL using pytds
    url = f"mssql+pytds://{user}:{password}@{server}/{database}"

    engine = create_engine(url)
    return engine.connect()
