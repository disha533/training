# schemas/schema.py
#
# Two independent models, one per domain:
#   - Student: rows in Oracle, managed by the students API.
#   - SearchDoc: rows in ClickHouse, managed by the search-docs API.
# They are not related to each other and don't share ids or fields
# other than happening to both have name/email.

from pydantic import BaseModel, EmailStr


class Student(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr
    branch: str
    year: int


class SearchDoc(BaseModel):
    id: int
    name: str
    email: EmailStr
    
class Course(BaseModel):
    id: int
    name: str
    duration_weeks: int