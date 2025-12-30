# date_posted.py
from flask import Blueprint, request, jsonify
from db import get_connection

dateposted_bp = Blueprint("dateposted", __name__)

@dateposted_bp.get("/date-posted")
def get_date_posted():
    date_posted = request.args.get("datePosted")
    scale = request.args.get("scale")
    type_ = request.args.get("type")

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM DatePosted WHERE 1=1"
    params = []

    # Correct column name: DatePosted
    if date_posted:
        query += " AND DatePosted = ?"
        params.append(date_posted)

    # Correct column name: Scale
    if scale:
        query += " AND Scale = ?"
        params.append(scale)

    # Correct column name: Type
    if type_:
        query += " AND Type = ?"
        params.append(type_)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = [
        dict(zip([column[0] for column in cursor.description], row))
        for row in rows
    ]

    return jsonify(results)
