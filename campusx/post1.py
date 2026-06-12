from pydantic import EmailStr,BaseModel,field_validator,Field,model_validator,computed_field
from typing import List,Optional,Annotated,Dict,Literal
from fastapi import FastAPI,Path,HTTPException,Query
import json

from campusx.patients_api import load_data

from fastapi.responses import JSONResponse

#       creating a pydantic model

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['P006','P007'])]
    name:Annotated[str,Field(...,min_length=3,max_length=50,description='Enter name in 50 chars',examples=['Nithish','Amit'])]
    city:Annotated[str,Field(...,min_length=3,max_length=20,description='Enter city in 20 chars',examples=['New Delhi','Amritsar'])]
    age:Annotated[int,Field(gt=0,le=120,examples=[34,120])]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
    height: Annotated[float, Field(...,gt=0.0,description='height of the patient in mtrs',examples=[0.5])] 
    weight: Annotated[float, Field(...,gt=0.0,description='weight of the patient in kgs',examples=[2.0])]


    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<30:
            return 'Normal'
        else:
            return 'Obese'
        # here bmi is itself computed so when the operator reaches the self.bmi it will trigger the bmi function so the calculated value will be passed


app=FastAPI()


def save_data(data):
    with open('campusx\patients.json','w') as file:
        json.dump(data,file)
        # erases the existing and keeps the present

@app.get('/')
def get():
    return{'message':'Welcome to world of FastAPI'}
@app.get('/data')
def show_data():
    data=load_data()
    return data


@app.post('/create')
def create_patient(patient:Patient):
    # loading the existing 
    data=load_data()

    # checking id existed 
    pid=patient.id.upper()
    if pid in data:
        raise HTTPException(status_code=400,detail='Patient already exist')
    
    # if not exist then add  but we got a pydantic object but the data is in json

    data[pid]=patient.model_dump(exclude=['id'])

    # saving it into the json file
    save_data(data)

    # return the json response

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})






