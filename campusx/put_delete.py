# update endpoint -/edit  HTTP Method-> PUT
# new pydantic model is required / why can't we use the previou one ?
# ans: there all those field were required where as now we dont know how many fields they want to edit
# so if we use them then it will expect all those fields

# edit/patient_id/request_body


from pydantic import EmailStr,BaseModel,field_validator,Field,model_validator,computed_field
from typing import List,Optional,Annotated,Dict,Literal
from fastapi import FastAPI,Path,HTTPException,Query
import json
from campusx.patients_api import load_data

from campusx.post1 import Patient
from fastapi.responses import JSONResponse


class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None,min_length=3,max_length=50,description='Enter name in 50 chars',examples=['Nithish','Amit'])]
    city:Annotated[Optional[str],Field(default=None,min_length=3,max_length=20,description='Enter city in 20 chars',examples=['New Delhi','Amritsar'])]
    age:Annotated[Optional[int],Field(default=None,gt=0,le=120,examples=[34,120])]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None,description='Gender of the patient')]
    height: Annotated[Optional[float], Field(default=None,gt=0.0,description='height of the patient in mtrs',examples=[0.5])] 
    weight: Annotated[Optional[float], Field(default=None,gt=0.0,description='weight of the patient in kgs',examples=[2.0])]
# when fields are optional then it should have default values

app=FastAPI()
@app.put('/edit/{patient_id}')
def update(patient_id:str,patient_update:PatientUpdate):
    data=load_data()
    pid=patient_id.upper()
    if pid not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    existing_data=data[pid]
    patient_info=patient_update.model_dump(exclude_unset=True)  # only the changed data will be dumped to json

    for key,val in patient_info.items():
        existing_data[key]=val
    

# existing_data -> pydantic object -> updating the value
    existing_data['id']=pid
    patient_pydantic_obj=Patient(**existing_data)

#  pydantic object  -. dictionary

    new_info=patient_pydantic_obj.model_dump(exclude='id')
    data[pid]=new_info


    with open('campusx\patients.json','w') as file:
        json.dump(data,file)
    
    return JSONResponse(status_code=200,content={'message':'succesfully updated the values'})



#                       DELETE

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    pid=patient_id.upper()
    data=load_data()
    if pid not in data:
        raise HTTPException(status_code=404,detail='patient not exist to delete')
    
    del data[pid]
    with open('campusx\patients.json','w') as file:
        json.dump(data,file)
    
    return JSONResponse(status_code=200,content={'message':'succesfully deleted the patient'})

