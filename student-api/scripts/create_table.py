# scripts/create_table.py
#
# Run once, manually, to create the STUDENTS table:
#   python -m scripts.create_table
#
# Uses the same pool mechanism as the app (init_pool/get_pool) instead of
# opening its own separate connection, so there's only ever one way to
# connect to Oracle in this whole project. Unlike the running app, this
# script isn't going through main.py's lifespan hook, so it calls
# init_pool() itself before use.

from db.oracle import init_pool, close_pool, get_pool

init_pool()
pool = get_pool()

connection = pool.acquire()
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE STUDENTS (
        ID NUMBER PRIMARY KEY,
        NAME VARCHAR2(100),
        AGE NUMBER,
        EMAIL VARCHAR2(100),
        BRANCH VARCHAR2(100),
        YEAR NUMBER
    )
    """
)
connection.commit()
print("Table created successfully!")

cursor.close()
pool.release(connection)
close_pool()
