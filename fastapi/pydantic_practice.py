from pydantic import BaseModel,EmailStr
from typing import List,Optional
class Patient(BaseModel):
    name:str
    age:int
    email:EmailStr
    weight:float
    allergies:Optional[List[str]]=None
patient_info={'name':"ABC","age":22,"email":"news@gmail.com","weight":45.6,"allergies":["pollen","dust"]}
patient1=Patient(**patient_info)
def display_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print("displayed")

display_data(patient1)