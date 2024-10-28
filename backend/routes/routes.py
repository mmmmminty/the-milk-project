from flask import jsonify, Blueprint, request
from database.tables.milk import fetch_milks, fetch_unverified_milks, create_milk, fetch_milk, update_milk, fetch_delete_milk
from database.tables.staff import create_nurse, fetch_nurse, link_nurse_to_baby, delete_nurse 
from database.tables.milk import add_additive_to_milk, fetch_additives, create_additive, fetch_all_additives, fetch_additive_by_name, update_additive_expiry_modifier
from database.tables.family import create_mother_and_baby, create_baby, delete_family, fetch_mothers, fetch_mother, fetch_all_babies, fetch_babies, fetch_baby, delete_family

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
    unverified_list = fetch_unverified_milks()
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

    updated_milk = update_milk(milk_id, verified_by, additives, defrosted)
    
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

    result = fetch_delete_milk(milk_id)
    
    if result:
        return jsonify({'message': 'Milk deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete milk or milk not found'}), 400
    

# Staff 
#given name and id the nurse is created 
@bp.route('/nurse/', methods=['POST'])
def add_nurse(): 
    data = request.get_json()

    nurse_id = data.get("id")
    nurse_name = data.get('name')
  
    if nurse_id is None | nurse_name is None:
        return jsonify({'error': 'Input Error'}), 400
   
    result = create_nurse(nurse_id, nurse_name)

    if result:
        return jsonify({'message': 'Nurse added successfully'}), 200
    else:
        return jsonify({'error': 'Bad request'}), 400
    
# Staff 
#given name and id the nurse is created 
@bp.route('/nurse/', methods=['GET'])
def get_nurse(): 
    id = request.args.get('id')

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_nurse(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Nurse not found'}), 400

@bp.route('/nurse/assign', methods=['POST'])
def assign_nurse(): 
    data = request.get_json()

    nurse_id = data.get("nurseId")
    baby_id = data.get('babyId')
  
    if nurse_id is None | baby_id is None:
        return jsonify({'error': 'Input Error'}), 400
   
    result = link_nurse_to_baby(nurse_id, baby_id)

    if result:
        return jsonify({'message': 'Assignment added successfully'}), 200
    else:
        return jsonify({'error': 'Bad request'}), 400
    

@bp.route('/nurse/assign', methods=['DELETE'])
def remove_nurse(): 
    id = request.args.get('id')
  
    if id is None:
        return jsonify({'error': 'Input Error'}), 400
   
    result = delete_nurse(id)

    if result:
        return jsonify({'message': 'Deleted successfully'}), 200
    else:
        return jsonify({'error': 'Bad request'}), 400
    
#additives 

@bp.route('/additive/', methods=['GET'])
def additive_get(): 
    id = request.args.get('id')

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_additives(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Additive not found'}), 400

# inputs additive, amount, milk id 
@bp.route('/milk/additive/', methods=['POST'])
def additive_post(): 
    data = request.get_json()

    additive = data.additive
    amount = data.amount 
    milk_id = data.milkId

    result = add_additive_to_milk(additive, amount, milk_id)

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_additives(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Additive request error'}), 400

#family 

@bp.route('/family/register/', methods=['POST'])
def family_register(): 
    data = request.get_json()

    mrn = data.mrn
    mother_name = data.motherName 
    baby_name = data.babyName

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = create_mother_and_baby(mrn, mother_name, baby_name)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Request error'}), 400

@bp.route('/family/baby/', methods=['POST'])
def baby_register(): 
    data = request.get_json()

    mother_id = data.motherId
    mrn = data.mrn
    baby_name = data.babyName

    result = create_baby(mother_id, mrn, baby_name)

    if mother_id is None | mrn is None | baby_name is None:
        return jsonify({'error': 'Input Error'}), 400
    
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Nurse not found'}), 400
    
@bp.route('/family/mother/', methods=['GET'])
def mother_get(): 
    id = request.args.get('id')

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_mother(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Nurse not found'}), 400

@bp.route('/family/baby/', methods=['GET'])
def baby_get(): 
    id = request.args.get('id')

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_baby(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'baby not found'}), 400
    
@bp.route('/family/babies/', methods=['GET'])
def babies_get(): 
    id = request.args.get('mother_id') # requests mothers ID

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_babies(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'request error'}), 400

@bp.route('/family/', methods=['DELETE'])
def family_delete(): 
    mrn = request.args.get('mrn')   
    result = delete_family(mrn)

    if mrn is None:
        return jsonify({'error': 'Input Error'}), 400
    
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Nurse not found'}), 400