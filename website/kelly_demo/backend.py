# // Milk Project website backend


# Milk Project website backend
# By Kelly C (15/10/2024)

from flask import Flask, render_template, request, jsonify
import sys
import psycopg2
import subprocess
import os


backend = Flask(__name__)

def connect_database():
    try:
        conn = psycopg2.connect(
            database="database",
            user="postgres",
            password="mypassword",
            host="localhost",
            port="5432"
        )
        print("database connection successful")
        return conn
    except Exception as err:
        print(f"database connection failed: {err}")
        sys.exit(1)

# /create
# @backend.route("/create", methods=["POST"])
# def create_qr_code():
#     data = request.get_json()
#     uuid =  data.get("uuid")
#     mothers_name =  data.get("mothers_name")
#     conn = connect_database()
#     cur = conn.cursor()
#     try:
#         cur.execute(
#             "INSERT INTO milks (uuid, mothers_name) VALUES (%s, %s)",
#             (uuid, mothers_name)
#         )
#         conn.commit()
#         return jsonify({"message": "Added successfully"})
#     except Exception as err:
#         conn.rollback()
#         return jsonify({"error": str(err)}), 500

@backend.route('/')
def index():
    return render_template('index.html')

@backend.route("/create", methods=["GET"])
def create():
    return "<h1>Create Page</h1>"
    

if __name__ == "__main__":
    try:
        backend.run(port=5001)
    finally:
        try:
            subprocess.run(["./backup_script"], check=True)
            print("backup successful")
        except subprocess.CalledProcessError as err:
            print("backup failed")