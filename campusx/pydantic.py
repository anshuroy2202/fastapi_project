# # def insert_patient_data(name,age):
# #     print(name,age)
# #     print("inserted into the database")

# # # lets imagine that this function is imported he can only see the signature 
# # # insert_patient_data(name,age) where name->any, age->any  so he passed


# # insert_patient_data("kanchana","fourthy four")

# # insert_patient_data("kanchana",44)

# # # here both run's hence it is the main  problem

# # def insert_patient_data1(name:str,age:int):  # type printing
# #     print(name,age)
# #     print("inserted into the database")


# # insert_patient_data1("kanchana","fourthy four")
# # # still runs it is just providing the info not the error hence it is also not the correct solution



# # #  dealing that using the exception handling
# # def insert_patient_data2(name:str,age:int):  # type printing
# #     if type(name)=='str' and type(age)=='int':
# #         print(name,age)
# #         print("inserted into the database")
# #     else:
# #         raise TypeError("Incorrect data type") 
    

# # insert_patient_data2("kanchana","fourthy four")  #(type validation)
# # # it is not scalable because we cant write this for each and every variable for every task like insertion or updation and also at the time of  deletion
# # # hence pydantic came into the picture

# # #  validation error is also solved by the pydantic beacuse age can't be -ve like that we need to check for all the variable 
# # # for this also we can use the pydantic for both type-data validation


from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

# # step -1 model is created
# class ContactDetails(BaseModel):
#     phone_no: str
#     email_id: EmailStr   #  str!= data validation
#     linkedln_url:Optional[AnyUrl]=None


# class Patient(BaseModel):
#     name: str
#     age: int
#     weight: float
#     married: bool
#     allergies: List[str]
#     contact_details: ContactDetails
#     spouse:Optional[List[str]]=None

# by default they are required fields
#  optional is used for that we define the deafult value


# # pydantic object is created

# # patient_info={'name':'nithish','age':30}
# patient1=Patient(**patient_info)  # unpacking
# #  if rules applied then object is return

# # calling
# def insert_patient_data2(patient:Patient):  # type printing
#     try:
#         print(patient.name,patient.age)
#         print(patient.married,patient.weight)
#         print(patient.contact_details)
#         print(patient.allergies)
#         print("inserted into the database") 
#     except Exception as e:
#         print("Incorrect Data Type")
#         print("ERROR!!",e)


# insert_patient_data2(patient1)

# print("Error generated")
# patient_info={'name':'nithish','age':'forutty'}
# patient12=Patient(**patient_info) 
# # insert_patient_data2(patient12)

# def update_patient_data(patient:Patient):
#     try:
#         print(patient.name,patient.age)
#         print("inserted into the database") 
#     except Exception as e:
#         print("Incorrect Data Type")
#         print("ERROR!!",e)

# # insert_patient_data2(patient12)

# # here we dont need to check the type for every task simply the basemodel / schema is deciding the type of the variable 
# #  it can also type caste like 'age':'30' into 'age':30 hence we didn't got the error there


# #                   complex

# patient_info= {
#     'name': 'nithish',
#     'age': 45,
#     'weight': -69.0,
#     'married': False,
#     'allergies': ['dengue', 'malaria', 'skin-disease'],
#     'contact_details': {
#         'phone_no': '9876543219',
#         'email_id': 'jaimahakal@gmail.com',
#         'linkedln_url':":https//www.google.com"
#     }
# }

# p1=Patient(**patient_info)
# insert_patient_data2(p1)

# custom data validation can be performed using the pydantic => Field function

class contactDetails(BaseModel):
    email_id:EmailStr
    phone_no:str
    linkedln_url:Optional[AnyUrl]=None

class Patient(BaseModel):
    # name:str=Field(min_length=3,max_length=50)
    name:Annotated[
        str,Field(min_length=3,max_length=50,description='Enter your name in 50 Chars',examples=['Nithish','Amit'])
    ]
    age:int=Field(gt=0,lt=120)
    weight:Annotated[float,Field(gt=0,strict=True)]
    married:Annotated[
        bool,
        Field(default=False,description='Are you married?')
    ]
    allergies:Annotated[List[str],Field(default=None,max_length=5)]
    contact_details:contactDetails

def insert_patient_data2(patient:Patient):  # type printing
    try:
        print(patient.name,patient.age)
        print(patient.married,patient.weight)
        print(patient.contact_details)
        print(patient.allergies)
        print("inserted into the database") 
    except Exception as e:
        print("Incorrect Data Type")
        print("ERROR!!",e)


patient_info= {
    'name': 'nithish',
    'age': 45,
    'weight': 69.0,
    'married': False,
    'allergies': ['dengue', 'malaria', 'skin-disease'],
    'contact_details': {
        'phone_no': '9876543219',
        'email_id': 'jaimahakal@gmail.com',
        'linkedln_url':"https://www.google.com"
    }
}

p1=Patient(**patient_info)
insert_patient_data2(p1)

# field functions can also be used for attaching the meta data  in the documentation 'Annotated is used'
# pydantic is type conversing th str to number  so using the strict we can stop that



