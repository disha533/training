# db/oracle.py
#
# ONLY responsibility: hand out an Oracle cursor to whoever needs one.
# No student-specific SQL lives here - that belongs in repositories/.
#
# --- Why a pool instead of one shared connection? ---
# The old code did:
#       connection = oracledb.connect(...)     # ONE connection, created once
#       cursor = connection.cursor()
#       connection.commit() / connection.rollback()
#
# commit() and rollback() apply to the WHOLE connection, not to a single
# cursor/request. If two requests hit the API at the same time and share
# that one connection, request B's commit() can commit request A's
# not-yet-finished work (or A's rollback can wipe out B's data). 
# The fix: a POOL. Each request borrows (acquires) its own connection for
# the duration of that request, and gives it back (releases) when done.
# commit()/rollback() then only ever affect that one request's connection.
#
# --- Why init_pool()/close_pool() instead of creating the pool at import ---
# Creating the pool as soon as this module is imported means a bad DB_DSN
# (or Oracle being down) blows up with a raw traceback the moment anything
# imports db.oracle - which could happen mid-import-chain, before FastAPI
# has even started listening. Instead, main.py calls init_pool() explicitly
# from a startup hook, so a connection failure surfaces as a clean "server
# failed to start" instead of an import-time crash, and close_pool() lets
# the app release connections cleanly on shutdown.

import oracledb
from contextlib import contextmanager
from config import DB_USER, DB_PASSWORD, DB_DSN

_pool = None


def init_pool():
    """Call once, from main.py's startup hook."""
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN,
            min=2,      # connections kept open at all times
            max=10,     # hard ceiling, extra requests wait for one to free up
            increment=1,
        )
    return _pool


def close_pool():
    """Call once, from main.py's shutdown hook."""
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def get_pool():
    """For callers (like scripts/) that need the pool object directly."""
    if _pool is None:
        raise RuntimeError(
            "Oracle pool not initialised - call init_pool() first "
            "(the app does this automatically at startup)."
        )
    return _pool


@contextmanager
def get_cursor(commit: bool = False):
    """
    Use as:  with get_cursor(commit=True) as cursor: ...

    Borrows a connection from the pool, gives you a cursor on it, and
    always returns the connection to the pool when the `with` block ends
    - even if an exception happened.
    """
    pool = get_pool()
    connection = pool.acquire()
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
        pool.release(connection)
