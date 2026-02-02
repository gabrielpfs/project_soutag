# src/ingest.py
import pandas as pd
import logging
from sqlalchemy.exc import SQLAlchemyError
import difflib
import re
from typing import List, Dict, Optional, Tuple

# -------------------------
# Leitura do CSV (robusta)
# -------------------------
def load_csv(csv_path: str,
             encoding: str = "utf-8",
             dtype: Optional[Dict] = None,
             parse_dates: Optional[List[str]] = None,
             low_memory: bool = True) -> pd.DataFrame:
    """
    Lê CSV com fallback de encoding e faz limpeza mínima de cabeçalhos.
    """
    try:
        df = pd.read_csv(csv_path, encoding=encoding, dtype=dtype, parse_dates=parse_dates, low_memory=low_memory)
    except UnicodeDecodeError:
        logging.warning("UTF-8 failed, trying latin1...")
        df = pd.read_csv(csv_path, encoding="latin1", dtype=dtype, parse_dates=parse_dates, low_memory=low_memory)

    # Limpeza básica de headers: strip + remover BOM
    df.columns = [col.strip().replace("\ufeff", "") for col in df.columns]
    logging.info(f"CSV loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

# -------------------------
# Helpers: normalizar nome
# -------------------------
def _normalize_colname(s: str) -> str:
    """normaliza para lowercase + underscores; remove caracteres não alfanuméricos"""
    s = str(s).strip().lower()
    s = re.sub(r'\s+', '_', s)                    # spaces -> underscore
    s = re.sub(r'[^a-z0-9_]', '_', s)             # remove chars inválidos
    s = re.sub(r'_+', '_', s)                     # colapsa underscores
    s = s.strip('_')
    return s

# -------------------------
# Validação avançada
# -------------------------
def validate_columns(df: pd.DataFrame,
                     expected_columns: List[str],
                     *,
                     normalize: bool = True,
                     rename: bool = False,
                     auto_fill_missing: bool = False,
                     fill_value = None,
                     case_sensitive: bool = False
                     ) -> Dict[str, List]:
    """
    Valida se todas expected_columns estão presentes.
    Retorna dict com info: {'missing':[], 'extra':[], 'renamed':{orig: new}, 'suggestions':{col: [cands]}}.
    - normalize: compara nomes normalizados (recomendado para CSVs externos).
    - rename: aplica renomeação no DataFrame (apenas se normalize=True).
    - auto_fill_missing: cria colunas faltantes com fill_value (útil em pipelines resilientes).
    """
    info = {'missing': [], 'extra': [], 'renamed': {}, 'suggestions': {}}

    orig_columns = list(df.columns)

    if normalize:
        normalized_map = {_normalize_colname(c): c for c in orig_columns}
        normalized_cols = set(normalized_map.keys())
        expected_norm_map = {_normalize_colname(c): c for c in expected_columns}
        expected_norm_set = set(expected_norm_map.keys())

        missing_norm = sorted(list(expected_norm_set - normalized_cols))
        extra_norm = sorted(list(normalized_cols - expected_norm_set))

        # preparar sugestões para cada coluna faltante
        for miss in missing_norm:
            # sugere com base nos nomes originais (não-normalizados), usando difflib
            candidates = difflib.get_close_matches(miss, list(normalized_map.keys()), n=3, cutoff=0.55)
            info['suggestions'][expected_norm_map[miss]] = [normalized_map[c] for c in candidates] if candidates else []

        # map missing back to expected original names
        info['missing'] = [expected_norm_map[n] for n in missing_norm]
        info['extra'] = [normalized_map[n] for n in extra_norm]

        # se rename=True, renomeia df.columns para a forma normalizada esperada (mantém original mapping)
        if rename:
            # criamos mapping: original_col -> normalized_expected_name (quando aplicável)
            rename_map = {}
            for norm, orig_expected in expected_norm_map.items():
                if norm in normalized_map:
                    orig_col = normalized_map[norm]
                    # renomeia para o expected original (ex: 'listed_in' => 'listed_in' ou 'listed in' conforme expected entram)
                    rename_map[orig_col] = orig_expected
            if rename_map:
                df.rename(columns=rename_map, inplace=True)
                info['renamed'] = rename_map

    else:
        # case_sensitive false => case-insensitive comparison
        if not case_sensitive:
            lower_cols = {c.lower(): c for c in orig_columns}
            missing = [c for c in expected_columns if c.lower() not in lower_cols]
            info['missing'] = missing
            info['extra'] = [c for c in orig_columns if c.lower() not in {e.lower() for e in expected_columns}]
        else:
            missing = [c for c in expected_columns if c not in orig_columns]
            info['missing'] = missing
            info['extra'] = [c for c in orig_columns if c not in expected_columns]

        # sugestões (basic)
        for miss in info['missing']:
            info['suggestions'][miss] = difflib.get_close_matches(miss, orig_columns, n=3, cutoff=0.6)

    # comportamento quando faltam colunas
    if info['missing']:
        msg = f"Missing columns detected: {info['missing']}. Suggestions: {info['suggestions']}"
        if auto_fill_missing:
            for col in info['missing']:
                df[col] = fill_value
            logging.warning(msg + " -> missing columns were auto-filled.")
            # limpamos 'missing' porque agora existem na df
            info['missing'] = []
        else:
            # não auto-fill => falha controlada
            logging.error(msg)
            raise ValueError(msg)

    logging.info("Column validation passed (no missing columns). Extra columns: %s", info['extra'])
    return info

# -------------------------
# Coerção/validação de tipos
# -------------------------
def validate_and_coerce_types(df: pd.DataFrame,
                              expected_types: Dict[str, str]) -> Dict[str, int]:
    """
    expected_types example: {'date_added':'datetime', 'release_year':'int', 'show_id':'str'}
    Retorna um dict com número de valores que não puderam ser convertidos por coluna.
    """
    result = {}
    for col, t in expected_types.items():
        if col not in df.columns:
            logging.warning("Column %s not in df, skipping type check.", col)
            result[col] = -1
            continue

        if t == 'datetime':
            before_na = df[col].isna().sum()
            df[col] = pd.to_datetime(df[col], errors='coerce')
            after_na = df[col].isna().sum()
            result[col] = int(after_na - before_na)
            logging.info("Coerced %s to datetime, new nulls: %d (delta %d)", col, after_na, result[col])

        elif t in ('int', 'float'):
            before_na = df[col].isna().sum()
            coerced = pd.to_numeric(df[col], errors='coerce')
            after_na = coerced.isna().sum()
            if t == 'int':
                # use nullable integer dtype
                df[col] = coerced.astype('Int64')
            else:
                df[col] = coerced.astype('float64')
            result[col] = int(after_na - before_na)
            logging.info("Coerced %s to %s, new nulls delta: %d", col, t, result[col])

        else:  # string or unknown - ensure dtype object
            df[col] = df[col].astype('object')
            result[col] = 0

    return result

# -------------------------
# Checagens simples de integridade
# -------------------------
def check_primary_key(df: pd.DataFrame, pk: str) -> Dict[str, int]:
    """
    Verifica nulls e duplicados na coluna pk.
    Retorna dict {'nulls': int, 'duplicates': int}
    """
    if pk not in df.columns:
        raise KeyError(f"Primary key column '{pk}' not found in dataframe.")

    nulls = int(df[pk].isna().sum())
    duplicates = int(df.duplicated(subset=[pk]).sum())

    if nulls > 0 or duplicates > 0:
        msg = f"Primary key '{pk}' integrity issue -> nulls: {nulls}, duplicates: {duplicates}"
        logging.error(msg)
        raise ValueError(msg)

    logging.info("Primary key check passed for '%s'. No nulls or duplicates.", pk)
    return {'nulls': nulls, 'duplicates': duplicates}

# -------------------------
# Ingestão para PostgreSQL (melhor performance com chunks)
# -------------------------
def ingest_to_postgres(df: pd.DataFrame, engine, table_name: str,
                       if_exists: str = 'replace', chunksize: int = 5000, method: Optional[str] = 'multi'):
    try:
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, chunksize=chunksize, method=method)
        logging.info(f"Data ingested into table '{table_name}' (rows: {len(df)})")
    except SQLAlchemyError as e:
        logging.exception(f"Error ingesting data: {e}")
        raise
