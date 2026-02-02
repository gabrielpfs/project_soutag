# src/transform.py

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.db import create_engine_postgres
from src.config import load_env
from src.logger import setup_logger

# -------------------------------------
# INITIAL SETUP
# -------------------------------------

logger = setup_logger()
load_env()
engine = create_engine_postgres()

chunk_size = 10000  # tamanho do chunk para ingestão escalável

# -----------------------------
# AUXILIARY FUNCTIONS
# -----------------------------

def load_raw_table(table_name="netflix_raw"):
    """Carrega a tabela raw do PostgreSQL"""
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    logger.info(f"✅ Loaded raw table with {df.shape[0]} rows and {df.shape[1]} columns")
    return df


def clean_titles(df):
    """Executa padronização de colunas e tratamento de valores"""
    df.columns = [col.lower() for col in df.columns]
    logger.info("✅ Column names converted to snake_case")

    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    logger.info("✅ date_added converted to datetime")

    df[['duration_value', 'duration_unit']] = df['duration'].str.extract(r'(\d+)\s*(\w+)')
    df['duration_value'] = df['duration_value'].astype('Int64')
    logger.info("✅ duration split into duration_value and duration_unit")

    df['country'] = df['country'].fillna('not_specified').str.lower().str.strip()
    df['rating'] = df['rating'].fillna('not_rated').str.lower().str.strip()
    df['type'] = df['type'].str.lower().str.strip()
    df['listed_in'] = df['listed_in'].str.lower().str.strip()
    logger.info("✅ Missing values filled and categorical columns normalized")

    logger.info("✅ Columns cleaned and normalized")
    return df


def save_clean_table(df, table_name="titles_clean"):
    """Salva tabela limpa no PostgreSQL"""
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=chunk_size)
        logger.info(f"✅ '{table_name}' saved in PostgreSQL with {df.shape[0]} records")
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to save '{table_name}': {e}")
        raise


# -----------------------------
# PRIMARY KEY
# -----------------------------

def create_primary_key_titles_clean():
    """Cria PK em titles_clean(show_id) com commit explícito"""
    query = "ALTER TABLE titles_clean ADD CONSTRAINT pk_titles_clean_show PRIMARY KEY (show_id);"
    try:
        with engine.begin() as conn:  # commit explícito
            conn.execute(text(query))
        logger.info("✅ Primary key created on titles_clean(show_id)")
    except SQLAlchemyError as e:
        logger.warning(f"⚠️ Primary key creation skipped or failed: {e}")


# -----------------------------
# NORMALIZATIONS
# -----------------------------

def create_titles_by_country(df, table_name="titles_by_country"):
    """Cria tabela título × país"""
    countries = df[['show_id','country']].copy()
    countries = countries.assign(country=countries['country'].str.split(','))
    countries = countries.explode('country')
    countries['country'] = countries['country'].str.strip()

    # Remove duplicados para não quebrar FK
    countries = countries.drop_duplicates(subset=['show_id', 'country'])

    try:
        countries.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=chunk_size)
        logger.info(f"✅ '{table_name}' saved in PostgreSQL with {countries.shape[0]} records")
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to save '{table_name}': {e}")
        raise
    return countries


def create_titles_by_genre(df, table_name="titles_by_genre"):
    """Cria tabela título × gênero"""
    genres = df[['show_id','listed_in']].copy()
    genres = genres.assign(genre=genres['listed_in'].str.split(','))
    genres = genres.explode('genre')
    genres['genre'] = genres['genre'].str.strip()

    # Remove duplicados para não quebrar FK
    genres = genres.drop_duplicates(subset=['show_id', 'genre'])

    try:
        genres.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=chunk_size)
        logger.info(f"✅ '{table_name}' saved in PostgreSQL with {genres.shape[0]} records")
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to save '{table_name}': {e}")
        raise
    return genres


# -----------------------------
# FOREIGN KEYS
# -----------------------------

def create_foreign_keys():
    """Cria FKs entre tabelas normalizadas e titles_clean"""
    queries = [
        """
        ALTER TABLE titles_by_country
        ADD CONSTRAINT fk_titles_by_country_show
        FOREIGN KEY (show_id)
        REFERENCES titles_clean(show_id)
        ON DELETE CASCADE;
        """,
        """
        ALTER TABLE titles_by_genre
        ADD CONSTRAINT fk_titles_by_genre_show
        FOREIGN KEY (show_id)
        REFERENCES titles_clean(show_id)
        ON DELETE CASCADE;
        """
    ]
    try:
        with engine.begin() as conn:  # commit explícito
            for query in queries:
                conn.execute(text(query))
        logger.info("✅ Foreign keys created successfully")
    except SQLAlchemyError as e:
        logger.warning(f"⚠️ FK creation skipped or failed: {e}")


# -----------------------------
# VALIDATIONS
# -----------------------------

def validate_tables(df_clean, titles_by_country, titles_by_genre):
    """Valida registros, nulos e duplicados"""
    logger.info("🔎 Running post-transformation validations...")

    logger.info(f"titles_clean: {df_clean.shape[0]} records, {df_clean.isnull().sum().to_dict()} nulls, {df_clean.duplicated().sum()} duplicates")
    logger.info(f"titles_by_country: {titles_by_country.shape[0]} records, {titles_by_country.isnull().sum().to_dict()} nulls, {titles_by_country.duplicated().sum()} duplicates")
    logger.info(f"titles_by_genre: {titles_by_genre.shape[0]} records, {titles_by_genre.isnull().sum().to_dict()} nulls, {titles_by_genre.duplicated().sum()} duplicates")


# -----------------------------
# COMPLETE PIPELINE
# -----------------------------

def run_transform():
    logger.info("🚀 Starting ETL: Transformation & Modeling")

    # 1️⃣ Carregar raw
    df_raw = load_raw_table()

    # 2️⃣ Limpeza e padronização
    df_clean = clean_titles(df_raw)

    # 2.1️⃣ Salvar tabela limpa
    save_clean_table(df_clean)

    # 2.2️⃣ Criar PRIMARY KEY
    create_primary_key_titles_clean()

    # 3️⃣ Criar tabelas normalizadas
    titles_by_country = create_titles_by_country(df_clean)
    titles_by_genre = create_titles_by_genre(df_clean)

    # 4️⃣ Criar FKs
    create_foreign_keys()

    # 5️⃣ Validações pós-transformação
    validate_tables(df_clean, titles_by_country, titles_by_genre)

    # Logs de verificação
    logger.info("✅ First 5 records in titles_by_country:")
    logger.info(titles_by_country.head(5).to_dict(orient="records"))

    logger.info("✅ First 5 records in titles_by_genre:")
    logger.info(titles_by_genre.head(5).to_dict(orient="records"))

    logger.info("✅ ETL: Transformation & Modeling completed successfully!")


# -------------------------------------
# DIRECT EXECUTION
# -------------------------------------

if __name__ == "__main__":
    run_transform()
