from database import connection

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE STUDENTS (
    ID NUMBER PRIMARY KEY,
    NAME VARCHAR2(100),
    AGE NUMBER,
    EMAIL VARCHAR2(100),
    BRANCH VARCHAR2(100),
    YEAR NUMBER
)
""")

connection.commit()

print("Table created successfully!")

cursor.close()
connection.close()