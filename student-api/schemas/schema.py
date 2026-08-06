from pydantic import BaseModel,EmailStr
class Student(BaseModel):
    id:int
    name:str
    age:int
    email:EmailStr
    branch:str
    year:int
