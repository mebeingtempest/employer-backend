# regions.py
from flask import Blueprint, request, jsonify
from db import get_connection

regions_bp = Blueprint("regions", __name__)

@regions_bp.get("/regions")
def get_regions():
    state = request.args.get("state")
    city = request.args.get("city")
    scale = request.args.get("scale")
    type_ = request.args.get("type")

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM Regions WHERE 1=1"
    params = []

    if state:
        query += " AND state = ?"
        params.append(state)

    if city:
        query += " AND city = ?"
        params.append(city)

    if scale:
        query += " AND scale = ?"
        params.append(scale)

    if type_:
        query += " AND type = ?"
        params.append(type_)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    return jsonify(results)
