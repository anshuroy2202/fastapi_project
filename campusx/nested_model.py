from pydantic import BaseModel
from typing import Dict

class Address(BaseModel):
    city:str
    state:str
    pincode:str

class Patient(BaseModel):
    name:str
    age:int
    address:Address
    gender:str='Male'

address_dict={
    'city':'gurgoan','state':'haryana','pincode':"122001"
}

add1=Address(**address_dict)
print(add1)

p_info={
    'name':'nithish',
    'age':30,
    'address':add1
}
p1=Patient(**p_info)
print(p1)
print(p1.name)
print(p1.address.pincode)
# here the address is used as the nested model
# now the address can be used any where for other purpose also because for employeee also the same address requirements will be present


# better organization of related data
#  reusability 
# readability increases and we can understand in a more better way
# validation :nested model are avlidated automatically no extra work is needed



#                           storing them in our required way
print('-'*55)
temp=p1.model_dump()  # convert the obj to py dictionary
print(type(temp),temp)
print('-'*55)
temp2=p1.model_dump_json()  # convert the obj to py json(str format)
print(type(temp2),temp2)
print('-'*55)
# we can only dump our required fields only
print("Only include the name and then the address field")
few=p1.model_dump(include=['name','address'])
print(few)
print('-'*55)
#  exclude is also present except that evrything 
print("Exclude the age field")
excpt=p1.model_dump(exclude=['age'])
print(excpt)
print('-'*55)
print("Exclude the state and age fields")
result = p1.model_dump(
    exclude={
        'age':True,   # beause the age is not a dictionary but exclude is dictionary so it will expect the key:value pair
        'address': {'state'}
    }
)

print(result)

#  to remove the gender 
p2=Patient(**patient_dict)
print(p2.model_dump(exclude_unset=True)) 
# due to this the gender is not given at the obj creation time so it will not even set the defualt value