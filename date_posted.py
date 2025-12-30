# date-posted.py
from flask import Blueprint, request, jsonify
from db import get_connection

dateposted_bp = Blueprint("dateposted", __name__)

@dateposted_bp.get("/date-posted")
def get_date_posted():
    date_range = request.args.get("dateRange")
    scale = request.args.get("scale")
    type_ = request.args.get("type")

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM DatePosted WHERE 1=1"
    params = []

    if date_range:
        query += " AND DateRange = ?"
        params.append(date_range)

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
