import unittest
from database_test import database_tests
from database.database import initdb
from app import run_server
from logger_config import logger

### MAIN APPLICATION ###
if __name__ == "__main__":
    logger.info("Starting the application")
    
    # Initialize the database
    initdb()

    # runner = unittest.TextTestRunner()
    # runner.run(database_tests())

    run_server()
