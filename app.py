from flask import Flask, request, jsonify
import os
import pyodbc

from regions import regions_bp
from industries import industries_bp
from date_posted import dateposted_bp 

app = Flask(__name__)

app.register_blueprint(regions_bp)
app.register_blueprint(industries_bp)
app.register_blueprint(dateposted_bp)

# --- Database connection helper ---
def get_connection():
    base_conn_str = os.getenv("CONNECTION_STRING")

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

        results = set()

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
