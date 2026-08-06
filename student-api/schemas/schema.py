from typing import Optional
from pydantic import BaseModel,EmailStr
class Student(BaseModel):
    id:int
    name:str
    age:int
    email:EmailStr
    branch:str
    year:int

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    branch: Optional[str] = None
    year: Optional[int] = None