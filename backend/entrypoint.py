import os
from database.database import initdb
from app import run_server

from utils.logger_config import logger

os.chdir(os.path.dirname(os.path.abspath(__file__)))

### MAIN APPLICATION ###
if __name__ == "__main__":
    logger.info("Starting the application")
    
    # Initialize the database
    initdb()

    # Run the server
    run_server()
