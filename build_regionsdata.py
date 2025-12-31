import pyodbc
import json

# -----------------------------------------
# 1. Your SQL connection string
#    (Paste your existing working connection string here)
# -----------------------------------------
CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:employer-search.database.windows.net,1433; Database=employersearch; Uid=Selfaryadmin; Pwd=akdivHYF23#%@; Encrypt=yes; TrustServerCertificate=no; Connection Timeout=30;"


# -----------------------------------------
# 2. Connect to SQL Server
# -----------------------------------------
conn = pyodbc.connect(CONNECTION_STRING)
cursor = conn.cursor()


# -----------------------------------------
# 3. Query your full dataset
#    Replace 'YourTable' with your actual table name
# -----------------------------------------
cursor.execute("""
    SELECT 
        City_Town_Other,
        EmployerLink,
        EmployerName,
        ID,
        Population,
        Scale,
        State,
        Type
    FROM Regions
""")

rows = cursor.fetchall()


# -----------------------------------------
# 4. Convert SQL rows → list of dictionaries
# -----------------------------------------
columns = [column[0] for column in cursor.description]

data = [dict(zip(columns, row)) for row in rows]


# -----------------------------------------
# 5. Save to /public/regionsdata.json
# -----------------------------------------
with open("../frontend/public/regionsdata.json", "w") as f:
    json.dump(data, f, indent=2)

print("regionsdata.json created successfully!")
