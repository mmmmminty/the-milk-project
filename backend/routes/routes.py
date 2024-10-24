from flask import jsonify, Blueprint, request
from database.database import get_db_cursor
from database.milk.milk import fetch_milks, fetch_unverified_milk, create_milk, fetch_milk

# Create a blueprint for your routes
bp = Blueprint('routes', __name__)

@bp.route('/milks/', methods=['GET'])
def get_milks():
    milk_list = fetch_milks()
    return jsonify(milk_list)

#given a milk id in query string, returns the milk object combined with Mother and baby details 

@bp.route('/milk/', methods=['GET'])
def get_milk():
    milk_id = request.args.get('id')

    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400

    milk_instance = fetch_milk(milk_id)

    if (milk_instance is None):
        return jsonify({'error': 'Invalid Milk Id'}), 400
    
    return jsonify(milk_instance)

@bp.route('/milk/unverified', methods=['GET'])
def get_unverified_milk():
    unverified_list = fetch_unverified_milk()
    return jsonify(unverified_list)

@bp.route('/milk/', methods=['POST'])
def post_unverified_milk():
    data = request.get_json()

    mother_id = data.get('mother_id')
    baby_id = data.get('baby_id')
    expressed_date = data.get('expressed_date')
    frozen = data.get('frozen', False) 

    if mother_id is None:
        return jsonify({'error': 'Mother ID is required'}), 400
    if baby_id is None:
        return jsonify({'error': 'Baby ID is required'}), 400
    if expressed_date is None:
        return jsonify({'error': 'Expressed date is required'}), 400

    milkId = create_milk(mother_id, baby_id, expressed_date, frozen)
    return jsonify({'milk_id': milk_id}), 200