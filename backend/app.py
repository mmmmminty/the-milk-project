from flask import Flask, jsonify
from database.database import initdb, get_db_cursor  # Import your database initialization and cursor management
from logger_config import logger
from routes.routes import bp 

app = Flask(__name__)

app.register_blueprint(bp)

def run_server():
    logger.info("Starting the server")
    app.run(port=5001)  #change port if necessary 
    
