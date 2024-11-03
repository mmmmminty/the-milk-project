from flask import jsonify, Blueprint, request, render_template, send_file
from database.tables.milk import fetch_milks, fetch_unverified_milks, create_milk, fetch_milk, update_milk, delete_milk, fetch_unverified_milks_all
from database.tables.staff import create_nurse, fetch_nurse, link_nurse_to_baby, delete_nurse 
from database.tables.additives import add_additive_to_milk, fetch_additives, create_additive, fetch_all_additives, fetch_additive_by_name, update_additive_expiry_modifier
from database.tables.family import create_mother_and_baby, create_baby, delete_family, fetch_mothers, fetch_mother, fetch_all_babies, fetch_babies, fetch_baby, delete_family
from utils.label_maker import label_maker
from utils.qr_code import baby_qr_code_maker
from database.validation import validate, ValidationType 
import os

bp = Blueprint('routes', __name__)

@bp.route("/")
def Index(): 
    return render_template("index.html")

@bp.route("/match/")
def match(): 
    return render_template("its-a-match.html")

@bp.route("/notmatch/")
def not_match(): 
    return render_template("not-a-match.html")

@bp.route("/milkinfo/")
def milk_info(): 
    return render_template("log-milk-info.html")

@bp.route("/milkmum/")
def milk_mum(): 
    return render_template("log-milk-mum.html")

@bp.route("/patientbaby/")
def milk_nurse(): 
    return render_template("log-milk-nurse.html")

@bp.route("/milknurse/")
def patient_baby(): 
    return render_template("log-patient-baby.html")

@bp.route("/matcher/")
def scanner(): 
    return render_template("matcher.html")

@bp.route('/milks/', methods=['GET'])
def get_milks():
    milk_list = fetch_milks()
    return jsonify(milk_list)

@bp.route('/milk/<milk_id>')
def milk_info_page(milk_id):
    return render_template("log-milk-info.html", milk_id=milk_id)

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
    mother_id = request.args.get('id')
    unverified_list = fetch_unverified_milks(mother_id)
    return jsonify(unverified_list)

@bp.route('/milk/unverifiedlist', methods=['GET'])
def get_unverified_milk_all():
    nurse_id = request.args.get('id')
    unverified_list = fetch_unverified_milks_all(nurse_id)
    return jsonify(unverified_list)

@bp.route('/milk/verify', methods=['PUT'])
def put_verify_milk():
    data = request.get_json()
    milk_id = data.get("milk_id")
    nurse_id = data.get("nurse_id")
    
    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400
    
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
    #baby_id = data.get('baby_id')
    expressed_date = data.get('expressed_date')
    frozen = data.get('frozen', False) 

    if mother_id is None:
        return jsonify({'error': 'Mother ID is required'}), 400
    # if baby_id is None:
    #     return jsonify({'error': 'Baby ID is required'}), 400
    if expressed_date is None:
        return jsonify({'error': 'Expressed date is required'}), 400

    milk_id = create_milk(mother_id, None , expressed_date, None, frozen)
    return jsonify({'milk_id': milk_id}), 200

# updates milk id, with parameters additives, defrost, verify 
@bp.route('/milk/', methods=['PUT'])
def server_update_milk():
    data = request.get_json()

    milk_id = data.get('milk_id') 

    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400
    
    expiry = data.get('expiry')
    expressed = data.get('expressed')
    volume = data.get('volume')
    frozen = data.get('frozen')
    defrosted = data.get('defrosted')
    fed = data.get('fed')
    verified_by = data.get('verified_by')
    #additives = data.get('additives') #[additive1, additive2], optional

    updated_milk = update_milk(milk_id, expiry, expressed, volume, frozen, defrosted, fed, verified_by)
    
    if updated_milk:
        return jsonify({'message': 'Milk updated successfully', 'milk': updated_milk}), 200
    else:
        return jsonify({'error': 'Failed to update milk or milk not found'}), 400

#query string gives milk id, milk id is deleted 

@bp.route('/milk/', methods=['DELETE'])
def server_delete_milk():
    milk_id = request.args.get('id')

    if milk_id is None:
        return jsonify({'error': 'Milk ID is required'}), 400

    result = delete_milk(milk_id)
    
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
  
    if nurse_id is None or nurse_name is None:
        return jsonify({'error': 'Input Error'}), 400
   
    result = create_nurse(nurse_id, nurse_name)

    if result:
        return jsonify({'message': 'Nurse added successfully'}), 200
    else:
        return jsonify({'error': 'Bad request'}), 400
    
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

    nurse_id = data.get("nurse_id")
    baby_id = data.get('baby_id')
  
    if nurse_id is None or baby_id is None:
        return jsonify({'error': 'Input Error'}), 400
   
    result = link_nurse_to_baby(nurse_id, baby_id)

    if result:
        return jsonify({'message': 'Assignment added successfully'}), 200
    else:
        return jsonify({'error': 'Bad request'}), 400
    

@bp.route('/nurse/', methods=['DELETE'])
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
    id = request.args.get('milk_id')

    if id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_additives(id)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Additive not found'}), 400

# inputs additive, amount, milk id 
@bp.route('/milk/additive/', methods=['POST'])
def add_additive(): 
    data = request.get_json()

    milk_id = data.get("milk_id")
    additive = data.get('additive')
    amount = data.get('amount')

    if milk_id is None or additive is None or amount is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = add_additive_to_milk(additive, amount, milk_id)

    if result:
        return jsonify({'successfully added additive to milk!'}), 200
    else:
        return jsonify({'error': 'Invalid request'}), 400

@bp.route('/validate/', methods=['GET'])
def server_validate(): 
    milk_id = request.args.get('milk_id')
    baby_id = request.args.get('baby_id')

    if milk_id is None or baby_id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    validation_type, extra_info  = validate(milk_id, baby_id)

    if validation_type == ValidationType.ERR_NOT_EXPRESSED_FOR:
        return jsonify({
            'status': validation_type.value,
            'true_baby_id': extra_info
        }), 200
    elif validation_type == ValidationType.ERR_EXPIRED:
        return jsonify({
            'status': validation_type.value,
            'expiry_date': extra_info.strftime("%Y-%m-%d %H:%M:%S")  
        }), 200
    elif validation_type == ValidationType.ERR_CONTAINS_ALLERGEN:
        return jsonify({
            'status': validation_type.value,
            'allergens': extra_info  
        }), 200
    elif validation_type == ValidationType.OK_VALID_FEED:
        return jsonify({
            'status': validation_type.value,
            'message': 'Milk is safe for the baby'
        }), 200
    else:
        return jsonify({'error': 'Unexpected validation outcome'}), 500

#family 

@bp.route('/family/register/', methods=['POST'])
def family_register(): 
    data = request.get_json()

    mrn = data.get("mrn")
    mother_name =  data.get("mother_name")
    baby_name = data.get("baby_name")

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

    mother_id = data.get("mother_id")
    mrn = data.get("mrn")
    baby_name = data.get("baby_name")

    result = create_baby(mother_id, mrn, baby_name)

    if mother_id is None or mrn is None or baby_name is None:
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
    mrn = request.args.get('mrn')

    if mrn is None:
        return jsonify({'error': 'Input Error'}), 400
    
    result = fetch_baby(mrn)
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'error': 'baby not found'}), 400
    
@bp.route('/family/babies/', methods=['GET'])
def babies_get(): 
    id = request.args.get('mother_id')
    
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
    
@bp.route('/print/', methods=['POST'])
def make_label(): 
    data = request.get_json()
    mother_id = data.get('mother_id')
    expressed_date = data.get('expressed_date')
    baby_MRN = data.get('baby_id')
    embedded_image_path = data.get('embedded_image_path')
    frozen = data.get('frozen', False) 

    milk_ids = []
    for x in range(14):
        milk_id = create_milk(mother_id, None, expressed_date, None, frozen)
        milk_ids.append(milk_id)
    result = label_maker(mother_id, milk_ids, baby_MRN=baby_MRN, embedded_image_path=embedded_image_path)

    if mother_id is None:
        return jsonify({'error': 'Input Error'}), 400
    
    if os.path.exists(result):
        return send_file(result, mimetype='image/png')
    else:
        return jsonify({'error': 'Label creation failed'}), 500
    
@bp.route('/print/baby', methods=['POST'])
def make_baby_qr(): 
    data = request.get_json()
    baby_MRN = data.get('baby_id')
    embedded_image_path = data.get('embedded_image_path')
    qr_file_path = f"./images/qr_{baby_MRN}.png"
    result = baby_qr_code_maker(baby_MRN, qr_file_path, embedded_image_path=embedded_image_path)

    if baby_MRN is None:
        return jsonify({'error': 'Input Error'}), 400
    
    if os.path.exists(result):
        return send_file(result, mimetype='image/png')
    else:
        return jsonify({'error': 'Label creation failed'}), 500