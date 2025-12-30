# industries.py
from flask import Blueprint, request, jsonify
from db import get_connection

industries_bp = Blueprint("industries", __name__)

@industries_bp.get("/industries")
def get_industries():
    industry = request.args.get("industry")
    subindustry = request.args.get("subindustry")
    scale = request.args.get("scale")
    type_ = request.args.get("type")

    conn = get_connection()
    cursor = conn.cursor()

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

    results = [
        dict(zip([column[0] for column in cursor.description], row))
        for row in rows
    ]

    return jsonify(results)
