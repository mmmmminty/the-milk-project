from flask import Flask, request, jsonify
from database.milk import addMilk

backend = Flask(__name__)

@backend.route("/milk", methods=["POST"])
def add_milk_entry():
    data = request.get_json()
    name = data.get("name")
    volume = data.get("volume")
    additives = data.get("additives")
    expiry = data.get("expiry")
    expressed_at = data.get("expressed_at")
    baby_of = data.get("Baby Of")

    try:
        addmilk.add_milk(name, volume, additives, expiry, expressed_at, expressed_by)
        return jsonify({"message": "Milk entry added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    backend.run(port=5001)
