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
        return "Connected to SQL. Woohoo!"
    except Exception as e:
        return str(e), 500

# --- Universal employer search route ---
@app.route("/search", methods=["GET"])
def search():
    try:
        query = request.args.get("q", "")

        conn = get_connection()
        cursor = conn.cursor()

        results = set()  # use a set to avoid duplicates

        # Search Regions table
        cursor.execute(
            "SELECT EmployerName FROM Regions WHERE EmployerName LIKE ?",
            f"%{query}%"
        )
        for row in cursor.fetchall():
            if row[0]:
                results.add(row[0])

        # Search Industries table
        cursor.execute(
            "SELECT EmployerName FROM Industries WHERE EmployerName LIKE ?",
            f"%{query}%"
        )
        for row in cursor.fetchall():
            if row[0]:
                results.add(row[0])

        # Search DatePosted table
        cursor.execute(
            "SELECT EmployerName FROM DatePosted WHERE EmployerName LIKE ?",
            f"%{query}%"
        )
        for row in cursor.fetchall():
            if row[0]:
                results.add(row[0])

        cursor.close()
        conn.close()

        return jsonify(list(results))

    except Exception as e:
        return jsonify({"error": str(e)}), 500
