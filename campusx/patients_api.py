from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()



def load_data():
    with open("campusx\patients.json",'r') as file:
        data=json.load(file)
        return data


#                               GET

@app.get("/")
def hello():
    return{
        'message':"Patient Management System API"
    }


@app.get("/about")
def about():
    return {
            "hospital_id": "H001",
            "hospital_name": "GreenLife Multispeciality Hospital",
            "city": "Bengaluru",
            "state": "Karnataka",
            "type": "Private",
            "total_beds": 250,
            "departments": [
              "Cardiology",
              "Orthopedics",
              "Neurology",
              "Pediatrics",
              "General Medicine"
            ],
            "emergency_available": True,
            "contact": {
              "phone": "+91-9876543210",
              "email": "contact@greenlifehospital.in"
            }
    }

# requesting all the users
@app.get('/view')
def view():
    data=load_data()
    return data

# getting any specific person using the id 
# @app.get('/patients/{patients_id}')
# def view_id(patients_id: str=Path(
#     ...,description='Patient ID (format: P001, P002, ...)'
# )
# ): # adding the path function for the validation rules 
# # def view_id(patients_id: str):   # paasing the patients id from the path params
#     data=load_data()
#     patients_id=patients_id.upper()
#     if patients_id in data:
#         return data[patients_id]
#     else:
#         return {'message':'patient not found or not exist'}


#   generating the status code
@app.get('/patients/{patients_id}')
def view_id(patients_id: str=Path(
    ...,description='Patient ID (format: P001, P002, ...)'
)
):
    data=load_data()
    patients_id=patients_id.upper()
    if patients_id in data:
        return data[patients_id]
    else:
        raise HTTPException(status_code=404,detail='patient not found or not exist')


#                            QUERY Parameters
# http://127.0.0.1:8000/sort?sort_by=bmi&order=asc
@app.get('/sort')
def sort_patients(sort_by:str=Query(
    ...,description='Sort on the basis of height ,weights,bmi'
),
order:str=Query('asc',description='Sort in asc or desc order')
):
    valid_feilds=['height','weight','bmi','age']
    if sort_by not in valid_feilds:
        raise HTTPException(
            status_code=400,detail=f'Inavlid field select from the {valid_feilds}'
        )
    
    if order not in ['desc','asc']:
        raise HTTPException(
            status_code=400,detail=f'Inavlid sorting  select from the {['desc','asc']}'
        )
    data=load_data()
    sort_order= True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data
