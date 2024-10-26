from flask import Flask, jsonify
from utils.constants import BACKEND_SERVER_PORT
from database.database import initdb, get_db_cursor  # Import your database initialization and cursor management
from utils.logger_config import logger
from routes.routes import bp 

app = Flask(__name__)

app.register_blueprint(bp)

def run_server():
    logger.info("Starting the server")
    app.run(port=BACKEND_SERVER_PORT)  #change port if necessary 
    