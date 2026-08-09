# db/clickhouse.py
#
# ONLY responsibility: connect to ClickHouse and make sure the
# search_docs table exists. No embedding/query logic here - that
# belongs in repositories/vector_repository.py. This mirrors
# db/oracle.py on purpose: SQL and vector storage are two completely
# separate, unrelated modules - neither imports the other, and their
# tables hold different, unlinked data.

import clickhouse_connect
import config

client = clickhouse_connect.get_client(
    host=config.CLICKHOUSE_HOST,
    port=config.CLICKHOUSE_PORT,
    username=config.CLICKHOUSE_USER,
    password=config.CLICKHOUSE_PASSWORD,
    database=config.CLICKHOUSE_DATABASE,
)


def init_vector_table():
    """
    Creates the search_docs table if it doesn't exist yet. Safe to call
    every time the app starts (CREATE TABLE IF NOT EXISTS is a no-op if
    it's already there).
    """
    client.command(
        """
        CREATE TABLE IF NOT EXISTS search_docs (
            id UInt32,
            name String,
            email String,
            embedding Array(Float32)
        ) ENGINE = MergeTree()
        ORDER BY id
        """
    )
