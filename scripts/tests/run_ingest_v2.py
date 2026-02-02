# scripts/run_ingest.py

import sys
import logging
from src.config import load_env
from src.logger import setup_logger
from src.db import create_engine_postgres
from src.ingest import load_csv, validate_columns, ingest_to_postgres

def main(csv_path='../data/netflix_titles.csv', table_name='netflix_raw'):
    logger = setup_logger()
    try:
        load_env()
        engine = create_engine_postgres()
        df = load_csv(csv_path)
        expected_columns = [
            'show_id','type','title','director','cast','country',
            'date_added','release_year','rating','duration','listed_in','description'
        ]
        validate_columns(df, expected_columns)
        ingest_to_postgres(df, engine, table_name)
        logger.info("Ingestion completed successfully!")
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
