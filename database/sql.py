import os
import pandas as pd
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from config import Config
from sqlalchemy import text

def get_engine():  
    return create_engine(Config.DATABASE_URL)

def get_db(engine):
    schema = os.getenv("DB_SCHEMA")
    include = os.getenv("INCLUDE_TABLES")
    return SQLDatabase(
        engine,
        schema=schema,
        include_tables=[t.strip() for t in include.split(",")] if include else None,
    )

def run_sql(engine, sql: str) -> pd.DataFrame:
    with engine.begin() as conn:
        if sql.strip().lower().startswith("select"):
            return pd.read_sql(sql, conn)
        else:
            conn.execute(text(sql))
            return pd.DataFrame()
