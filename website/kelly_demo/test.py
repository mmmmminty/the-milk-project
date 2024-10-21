from flask import Flask, request, jsonify
import subprocess
import os
import psycopg2
import sys

backend = Flask(__name__)

def exec_database():
    try:
        result = subprocess.run(
            ['psql', '-U', 'postgres', '-f', "database.sql"],
            check=True, text=True, capture_output=True
        )
        print("running database successfully")
        print(result.stdout)
    except Exception as err:
        print(f"running database failed: {err}")
        sys.exit(1)

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

if __name__ == '__main__':
    data = sys.argv
    uuid =  data[1]
    mothers_name =  data[2]
    print(uuid)
    print(mothers_name)
    conn = connect_database()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO milks (uuid, mothers_name) VALUES (%s, %s)",
            (uuid, mothers_name)
        )
        conn.commit()
        print("Added successfully")
    except Exception as err:
        conn.rollback()
        print("Failed")

    cur.close()
    conn.close()