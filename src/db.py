# src/db.py

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import logging

def create_engine_postgres():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        logging.info("Database engine created successfully.")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Error creating database engine: {e}")
        raise
