import json
from fastapi import FastAPI,Path,HTTPException,Query
app=FastAPI()
def get_data():
    with open("patients.json","r") as file:
        data=json.load(file)
    return data
@app.get("/")
def home():
    return {'message':'Patient Management System API'}
@app.get("/about")
def about():
    return {'message':"This is a demo of FASTAPI that perform CRUD on patient records"}
@app.get("/view")
def view():
    data=get_data()
    return data
@app.get("/patients/{patient_id}")
def view_patient(patient_id:str=Path(...,description="ID of the patient",example="P001")):
    data=get_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")
@app.get("/sort")
def sorted_data(sort_by:str=Query(...,description="Sort on basis of height.weight,bmi"), order:str=Query(default="asc",description="Ascending or Descending(asc/desc)")):
    data=get_data()
    valid_params=["bmi","height","weight"]
    if sort_by not in valid_params:
        raise HTTPException(status_code=400,detail="Invalid value given must be height,weight or bmi")
    if (order!="asc" and order!="desc"):
        raise HTTPException(status_code=400,detail="Invalid value given must be asc or desc")
    value_curr=False
    if order=="desc":
        value_curr=True
    
    sorted_data=sorted(data.values(),key=lambda x:x[sort_by],reverse=value_curr)
    return sorted_data