# scripts/test_connection.py

import sys
import os
from sqlalchemy import text
import logging

# ---------------------------------------------
# Adiciona a pasta raiz do projeto ao sys.path
# Isso permite importar src.config e src.db corretamente
# ---------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Agora podemos importar os módulos internos
from src.config import load_env
from src.db import create_engine_postgres

# -------------------------------
# Configuração de logger
# -------------------------------
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    return logging.getLogger()

# -------------------------------
# Função principal de validação
# -------------------------------
def validate_postgres_connection(engine, test_table='netflix_raw'):
    logger = setup_logger()
    try:
        with engine.connect() as conn:
            logger.info("🔹 Conexão com PostgreSQL estabelecida ✅")

            # Lista todas as tabelas no schema public
            result = conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
            )
            tables = [row[0] for row in result]
            logger.info(f"Tabelas existentes no schema public: {tables}")

            # Verifica se a tabela de ingestão existe
            if test_table in tables:
                logger.info(f"Tabela '{test_table}' encontrada! Exibindo primeiras 5 linhas:")
                sample = conn.execute(text(f"SELECT * FROM {test_table} LIMIT 5;"))
                for row in sample:
                    logger.info(row)
            else:
                logger.warning(f"Tabela '{test_table}' não encontrada no banco.")
    except Exception as e:
        logger.error(f"❌ Falha na conexão ou consulta PostgreSQL: {e}")
        raise

# -------------------------------
# Execução do script
# -------------------------------
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("🔹 Iniciando teste completo de conexão com PostgreSQL...")

    try:
        # Carregar variáveis de ambiente
        env = load_env()
        logger.info("✅ Variáveis de ambiente carregadas com sucesso")

        # Criar engine de conexão
        engine = create_engine_postgres()
        logger.info("✅ Engine de conexão criada com sucesso")

        # Validar conexão e tabelas
        validate_postgres_connection(engine, test_table='netflix_raw')
        logger.info("✅ Teste de conexão finalizado com sucesso!")

    except Exception as e:
        logger.error(f"❌ Validação completa falhou: {e}")
        sys.exit(1)
