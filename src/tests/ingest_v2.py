# src/ingest.py
import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from io import StringIO
import os

# Optional progress bar; if not installed, you can remove tqdm usage
try:
    from tqdm import tqdm
except Exception:
    tqdm = lambda x, **k: x  # fallback: iterator passthrough

LOGGER = logging.getLogger(__name__)

def _try_read_csv(csv_path, read_kwargs):
    """
    Tenta ler CSV com utf-8 e, se falhar por encoding, tenta latin1.
    Retorna DataFrame ou TextFileReader (when chunksize set).
    """
    try:
        return pd.read_csv(csv_path, **read_kwargs)
    except UnicodeDecodeError:
        LOGGER.warning("UnicodeDecodeError: tentando encoding='latin1'")
        read_kwargs['encoding'] = 'latin1'
        return pd.read_csv(csv_path, **read_kwargs)

def load_csv(csv_path,
             usecols=None,
             dtype=None,
             parse_dates=None,
             na_values=None,
             encoding='utf-8',
             low_memory=False,
             chunksize=None):
    """
    Carrega CSV com fallback de encoding e opção de chunked reader.
    - chunksize: int => retorna TextFileReader (iterable of DataFrame)
    - sem chunksize => retorna DataFrame
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at {csv_path}")

    read_kwargs = dict(
        filepath_or_buffer=csv_path,
        usecols=usecols,
        dtype=dtype,
        parse_dates=parse_dates,
        na_values=na_values,
        encoding=encoding,
        low_memory=low_memory,
        chunksize=chunksize
    )
    LOGGER.info(f"Lendo CSV: {csv_path} (chunksize={chunksize})")
    df_or_reader = _try_read_csv(csv_path, read_kwargs)
    if chunksize:
        # can't know total rows reliably but we log that reader was created
        LOGGER.info("CSV carregado como iterador (chunksize ativo).")
    else:
        LOGGER.info(f"CSV carregado: {df_or_reader.shape[0]} linhas, {df_or_reader.shape[1]} colunas")
    return df_or_reader

def validate_columns(df_or_cols, expected_columns):
    """
    Valida se as colunas esperadas existem.
    Accepts DataFrame or iterable/list of column names.
    """
    if hasattr(df_or_cols, "columns"):
        cols = list(df_or_cols.columns)
    else:
        cols = list(df_or_cols)
    missing = [c for c in expected_columns if c not in cols]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    LOGGER.info("All expected columns are present.")

def _preprocess_df(df):
    """
    Pre-processamento leve:
    - strip nas colunas object
    - transformar header para snake_case (opcional aqui)
    - converter date_added para datetime (irá forçar coerce)
    """
    # strip strings
    obj_cols = df.select_dtypes(include=['object']).columns
    for c in obj_cols:
        df[c] = df[c].where(df[c].isnull(), df[c].str.strip())
    # parse date_added if present
    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    return df

def ingest_to_postgres(df_or_reader, engine, table_name, chunksize=5000, method='pandas'):
    """
    Ingestão robusta para Postgres.
    - df_or_reader: DataFrame ou TextFileReader (iterable of DF)
    - engine: SQLAlchemy engine
    - table_name: destino
    - chunksize: usado internamente nos inserts (quando via pandas)
    - method: 'pandas' (df.to_sql) ou 'copy' (psycopg2 COPY - mais rápido)
    """
    try:
        if method == 'copy' and isinstance(df_or_reader, str):
            # If user passed csv_path string, allow fast COPY
            _copy_csv_to_table(engine, df_or_reader, table_name)
            LOGGER.info(f"Data copied to table '{table_name}' via COPY.")
            return

        if hasattr(df_or_reader, "__iter__") and not isinstance(df_or_reader, pd.DataFrame):
            # chunked ingestion
            first = True
            for chunk in tqdm(df_or_reader, desc="Ingesting chunks"):
                chunk = _preprocess_df(chunk)
                if_exists_mode = 'replace' if first else 'append'
                chunk.to_sql(table_name, engine, if_exists=if_exists_mode,
                             index=False, method='multi', chunksize=chunksize)
                LOGGER.info(f"Chunk ingested: {len(chunk)} rows (mode={if_exists_mode})")
                first = False
        else:
            # single DataFrame ingestion
            df = df_or_reader if isinstance(df_or_reader, pd.DataFrame) else pd.DataFrame(df_or_reader)
            df = _preprocess_df(df)
            df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi', chunksize=chunksize)
            LOGGER.info(f"Data ingested into table '{table_name}' ({len(df)} rows).")
    except SQLAlchemyError as e:
        LOGGER.error(f"SQLAlchemyError while ingesting: {e}")
        raise
    except Exception as e:
        LOGGER.error(f"Unexpected error while ingesting: {e}")
        raise

def _copy_csv_to_table(engine, csv_path, table_name):
    """
    Fast path using psycopg2 COPY FROM STDIN.
    Requires that the target table already exists and user has privileges.
    """
    conn = engine.raw_connection()
    cur = conn.cursor()
    LOGGER.info("Using COPY for fast ingestion. Ensure table exists with correct schema.")
    with open(csv_path, 'r', encoding='utf-8') as f:
        # COPY ... FROM STDIN WITH CSV HEADER
        sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ','"
        cur.copy_expert(sql, f)
    conn.commit()
    cur.close()
    conn.close()
