from database.database import initdb
from app import run_server
from logger_config import logger

### MAIN APPLICATION ###
if __name__ == "__main__":
    logger.info("Starting the application")
    
    # Initialize the database
    initdb()

    run_server()
