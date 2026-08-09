# config.py
#
# The ONLY place that calls load_dotenv(). Earlier, both database.py and
# auth.py called load_dotenv() independently - harmless, but repeated and
# confusing (two "sources of truth" for env loading). Now every other file
# just does `from config import SOMETHING`.

import os
from dotenv import load_dotenv

load_dotenv()

# --- Oracle (SQL) ---
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DSN = os.getenv("DB_DSN")

# --- ClickHouse (vector DB) ---
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT"))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")

# --- Auth ---
API_TOKEN = os.getenv("API_TOKEN")
