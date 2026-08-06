from pydantic import BaseModel,EmailStr
class StudentCreate(BaseModel):
    id:int
    name:str
    age:int
    email:EmailStr
    branch:str
    year:int
