from flask import Flask, request, jsonify
import os
import pyodbc

app = Flask(__name__)

# --- Database connection helper ---
def get_connection():
    # Pull the base connection string from Azure App Service environment variables
    base_conn_str = os.getenv("CONNECTION_STRING")

    # Ensure the ODBC driver is included (Azure App Service supports ODBC Driver 18)
    conn_str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"{base_conn_str}"
    )

    return pyodbc.connect(conn_str)

# --- Root route ---
@app.route("/")
def home():
    return "Backend is running!"

@app.route("/testdb")
def testdb():
    try:
        conn = get_connection()
        return "Connected to SQL. Wooo!"
    except Exception as e:
        return str(e), 500

# --- Example search route ---
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT TOP 10 EmployerName FROM Employers WHERE EmployerName LIKE ?",
        f"%{query}%"
    )
    rows = cursor.fetchall()

    results = [row[0] for row in rows]

    cursor.close()
    conn.close()

    return jsonify(results)
