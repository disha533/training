
#
# Run once: python -m scripts.create_new_table
# create_all() is safe — it only creates tables that don't exist yet
# (checks first, like CREATE TABLE IF NOT EXISTS). It never alters or
# drops existing tables, including STUDENTS.

from db.sqlalchemydb import Base, engine
from models.course import CourseModel  # import so it registers with Base.metadata

Base.metadata.create_all(bind=engine)
print("New table created successfully!")