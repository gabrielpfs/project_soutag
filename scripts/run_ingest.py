# scripts/run_ingest.py

import sys
import os
import logging
from sqlalchemy import text  # ✅ necessário para SQL literal no SQLAlchemy 2.x

# ---------------------------------------------
# Adiciona a pasta raiz do projeto ao sys.path
# ---------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import load_env
from src.logger import setup_logger
from src.db import create_engine_postgres
from src.ingest import load_csv, validate_columns, ingest_to_postgres


def main(csv_path, table_name='netflix_raw'):
    logger = setup_logger()
    try:
        # Carregar variáveis de ambiente
        load_env()
        # Criar engine de conexão
        engine = create_engine_postgres()

        # Carregar CSV
        df = load_csv(csv_path)

        # Lista de colunas esperadas
        expected_columns = [
            'show_id', 'type', 'title', 'director', 'cast', 'country',
            'date_added', 'release_year', 'rating', 'duration',
            'listed_in', 'description'
        ]
        # Validar colunas
        validate_columns(df, expected_columns)

        # Ingestão no PostgreSQL
        ingest_to_postgres(df, engine, table_name)

        # ✅ Pós-ingestão: mostrar contagem de registros
        with engine.connect() as conn:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
            print(f"✅ Total de registros importados: {count}")

            # Mostrar 5 primeiros registros
            print("✅ Primeiros 5 registros:")
            result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 5"))
            for row in result:
                print(row)

        logger.info("✅Ingestion completed successfully!")

    except Exception as e:
        logger.error(f"❌Ingestion failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Caminho absoluto do CSV baseado na raiz do projeto
    csv_path = os.path.join(project_root, 'data', 'netflix_titles.csv')
    main(csv_path=csv_path)
