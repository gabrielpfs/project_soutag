# scripts/test_connection.py

import sys
import os
from sqlalchemy import text

# ---------------------------------------------
# Adiciona a pasta raiz do projeto ao sys.path
# Isso permite importar src.config e src.db corretamente
# ---------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Agora podemos importar os módulos internos
from src.config import load_env
from src.db import create_engine_postgres

def main():
    print("🔹 Iniciando teste de conexão com PostgreSQL...")

    # Carregar variáveis de ambiente
    try:
        env = load_env()
        print("✅ Variáveis de ambiente carregadas com sucesso")
    except Exception as e:
        print(f"❌ Falha ao carregar variáveis de ambiente: {e}")
        return

    # Criar engine de conexão
    try:
        engine = create_engine_postgres()
        print("✅ Engine de conexão criada com sucesso")
    except Exception as e:
        print(f"❌ Falha ao criar engine do PostgreSQL: {e}")
        return

    # Testar conexão com o banco
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Conexão testada com sucesso! Versão do PostgreSQL: {version}")
    except Exception as e:
        print(f"❌ Falha na conexão com o PostgreSQL: {e}")

if __name__ == "__main__":
    main()
