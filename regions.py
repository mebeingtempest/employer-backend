# regions.py
from flask import Blueprint, request, jsonify
from db import get_connection  # make sure this exists in db.py
import traceback

regions_bp = Blueprint("regions", __name__)

@regions_bp.get("/regions")
def get_regions():
    try:
        state = request.args.get("state")
        city = request.args.get("city")
        scale = request.args.get("scale")
        type_ = request.args.get("type")

        conn = get_connection()
        cursor = conn.cursor()

        # If you’re worried about size, you can add TOP N here:
        # query = "SELECT TOP 5000 * FROM Regions WHERE 1=1"
        query = "SELECT * FROM Regions WHERE 1=1"
        params = []

        if state:
            query += " AND State = ?"
            params.append(state)

        if city:
            query += " AND City_Town_Other = ?"
            params.append(city)

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
        # Log full traceback to your logs
        print("Error in /regions endpoint:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
