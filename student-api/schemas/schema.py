from pydantic import BaseModel
class StudentCreate(BaseModel):
    id:int
    name:str
    age:int
    email:str
    branch:str
    year:int
