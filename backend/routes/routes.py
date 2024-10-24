from flask import jsonify, Blueprint
from database.database import get_db_cursor

# Create a blueprint for your routes
bp = Blueprint('routes', __name__)

@bp.route('/get/milk', methods=['GET'])
def get_milk():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM Milk;")
        milk_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]  
        milk_list = [dict(zip(columns, row)) for row in milk_data]  

    return jsonify(milk_list)

@bp.route('/get/milk/unverified', methods=['GET'])
def get_unverified_milk():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM unverified_milk;")  
        unverified_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        unverified_list = [dict(zip(columns, row)) for row in unverified_data]

    return jsonify(unverified_list)

