# src/ingest.py

import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError

def load_csv(csv_path):
    df = pd.read_csv(csv_path)
    logging.info(f"CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def validate_columns(df, expected_columns):
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    logging.info("All expected columns are present.")

def ingest_to_postgres(df, engine, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data ingested into table '{table_name}'")
    except SQLAlchemyError as e:
        logging.error(f"Error ingesting data: {e}")
        raise
