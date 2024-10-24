from flask import Flask, jsonify
from psycopg2 import sql

app = Flask(__name__)

@app.route('/get/milk', methods=['GET'])
def get_milk():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM Milk;")
        milk_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]  
        milk_list = [dict(zip(columns, row)) for row in milk_data]  

    return jsonify(milk_list)

@app.route('/get/milk/unverified', methods=['GET'])
def get_unverified_milk():
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM unverified_milk;")  
        unverified_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        unverified_list = [dict(zip(columns, row)) for row in unverified_data]

    return jsonify(unverified_list)

if __name__ == '__main__':
    app.run(port=5001)
