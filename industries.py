# industries.py
from flask import Blueprint, request, jsonify
from db import get_connection
import traceback

industries_bp = Blueprint("industries", __name__)

@industries_bp.get("/industries")
def get_industries():
    try:
        industry = request.args.get("Industry")
        subindustry = request.args.get("Subindustry")
        scale = request.args.get("Scale")
        type_ = request.args.get("Type")

        conn = get_connection()
        cursor = conn.cursor()

        # query = "SELECT TOP 5000 * FROM Industries WHERE 1=1"
        query = "SELECT * FROM Industries WHERE 1=1"
        params = []

        if industry:
            query += " AND Industry = ?"
            params.append(industry)

        if subindustry:
            query += " AND Subindustry = ?"
            params.append(subindustry)

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
        print("Error in /industries endpoint:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
