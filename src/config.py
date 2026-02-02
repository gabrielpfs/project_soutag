# src/config.py

import os
from dotenv import load_dotenv

def load_env():
    """
    Carrega variáveis de ambiente do arquivo .env e valida se todas estão presentes.
    """
    # Caminho absoluto relativo ao arquivo atual
    dotenv_path = os.path.join(os.path.dirname(__file__), '../env/.env')
    if not os.path.exists(dotenv_path):
        raise FileNotFoundError(f".env file not found at {dotenv_path}")

    load_dotenv(dotenv_path=dotenv_path)

    # Variáveis obrigatórias
    required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    # Retorna as variáveis carregadas
    return {var: os.getenv(var) for var in required_vars}

def test_env():
    """
    Testa se todas as variáveis de ambiente estão carregadas corretamente.
    """
    try:
        env_vars = load_env()
        print("✅ All environment variables loaded successfully:")
        for key, value in env_vars.items():
            display_value = value if key != "DB_PASSWORD" else "*****"  # Mascarar senha
            print(f"{key}: {display_value}")
    except Exception as e:
        print(f"❌ Environment test failed: {e}")

# Executa o teste se rodar o script diretamente
if __name__ == "__main__":
    test_env()
