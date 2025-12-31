# date_posted.py
from flask import Blueprint, request, jsonify
from db import get_connection
import traceback

dateposted_bp = Blueprint("dateposted", __name__)

@dateposted_bp.get("/dateposted")   # <-- FIXED: matches frontend
def get_date_posted():
    try:
        date_posted = request.args.get("DatePosted")
        scale = request.args.get("Scale")
        type_ = request.args.get("Type")

        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM DatePosted WHERE 1=1"
        params = []

        if date_posted:
            query += " AND DatePosted = ?"
            params.append(date_posted)

        if scale:
            query += " AND Scale = ?"
            params.append(scale)

        if type_:
            query += " AND Type = ?"
            params.append(type_)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        conn.close()

        return jsonify(results)

    except Exception as e:
        print("Error in /dateposted endpoint:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
