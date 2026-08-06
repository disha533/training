# database.py
import oracledb
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

connection = oracledb.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dsn=os.getenv("DB_DSN")
)

@contextmanager
def get_cursor(commit: bool = False):
    cursor = connection.cursor()
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()