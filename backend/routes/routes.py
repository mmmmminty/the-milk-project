from flask import jsonify, Blueprint, request
from database.tables.milk import fetch_milks, fetch_unverified_milk, create_milk, fetch_milk, fetch_update_milk

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

@bp.route('/milk/verify', methods=['PUT'])
def put_verify_milk():
    milk_id = request.args.get('milk_id')
    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400
    
    nurse_id = request.args.get('nurse_id')
    if nurse_id is None:
        return jsonify({'error': 'Nurse ID is required'}), 400
    
    if update_milk(milk_id, verified_by=nurse_id):
        return jsonify({'message': 'Milk verified!'}), 200
    else:
        return jsonify({'error': 'Failed to verify milk'}), 400
        
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

    milk_id = create_milk(mother_id, baby_id, expressed_date, frozen)
    return jsonify({'milk_id': milk_id}), 200


#WHATEVERS UNDER HERE HAS NOT BEEN IMPLEMENTED 

# updates milk id, with parameters additives, defrost, verify 
@bp.route('/milk/', methods=['PUT'])
def update_milk():
    data = request.get_json()

    milk_id = data.get('id') 

    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400
    
    verified_by = data.get('verified_id') # verified id of nurse, optional
    additives = data.get('additives') #[additive1, additive2], optional
    defrosted = data.get('defrosted') # boolean, optional

    updated_milk = fetch_update_milk(milk_id, verified_by, additives, defrosted)
    
    if updated_milk:
        return jsonify({'message': 'Milk updated successfully', 'milk': updated_milk}), 200
    else:
        return jsonify({'error': 'Failed to update milk or milk not found'}), 400

#query string gives milk id, milk id is deleted 

@bp.route('/milk/', methods=['DEL'])
def delete_milk():
    milk_id = request.args.get('id')

    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400

    result = fetch_remove_milk(milk_id)
    
    if result:
        return jsonify({'message': 'Milk deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete milk or milk not found'}), 400