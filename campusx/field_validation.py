# field validator  and field values transformation 
# ex. there is  a thing like where you have to check the  inpu and according to that they are processed next
# here only hdfc bank employee are being cured at a discount prize

from pydantic import EmailStr,BaseModel,field_validator,Field,model_validator,computed_field
from typing import List,Optional,Annotated,Dict

#  we need a method for field validation and that method is a decorator

class Contact(BaseModel):
    emergency:Optional[str]=None
    address:str
class Person(BaseModel):
    email_id:EmailStr
    name:Annotated[
        str,
        Field(default='Unknown Name',min_length=3,max_length=50,description='Enter you name under 50 chars')
    ]
    age:int
    contact:Contact
    weight:float
    height:float

    @field_validator('email_id')  # field name
    @classmethod

    def email_validator(cls,email_id_value):
        valid_domains=['hdfc.com','icici.com']
        # abc12@gmail.com   we need this part 'gmail.com'  to check

        domain_name=email_id_value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return email_id_value

    
    @field_validator('name')
    @classmethod
    def name_transformer(cls,name_val):
        return name_val.upper()

    @field_validator('age')#,'''mode='before''')
    # @classmethod
    def age_validator(cls,age_val):
        if 0<age_val<100:
            return age_val
        
        raise ValueError("Age should be between 0 to 100")
    

    @model_validator(mode='after') # here field name is not required because we are not working on one field value
    def emergency_contact(model):
        if model.age>60 and 'emergency' not in model.contact:
            raise ValueError("patients older than 60 must have the emergency number")

        return model


    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi









# p1_info={
#     'email_id':'anshu@gmail.com'
# }
p1_info={
    'email_id':'anshu@hdfc.com',
    'name':'anshu kumar',
    'age':'47',
    'weight':75.5,
    'height':5.11,
    'contact':{
        'address':'New Delhi'
    }
}
p2_info={
    'email_id':'anshu@hdfc.com',
    'name':'anshu kumar',
    'age':'67',
    'contact':{
        'address':'New Chennai'
    }
}
# calculate_bmi=2.89 is the key not the bmi  hence make the function bmi
p1=Person(**p1_info)  # at this step only all the validations happens
print(p1)

#  mode is by default 'after' hence due to this 1st it type cast them and then it process
#  if it is mode='before' it will get the value 1st and then type conversion 
# hence we got the error for age='47' because it is a string and due to mode='before' the type conversion doesn't happened before the value evaluation
# TypeError: '<' not supported between instances of 'int' and 'str'

# model validator is used to validate multiple values at once where as you can see that the field validator does only for one variable

# computed field 
#  the user doest calculate them the programmer will compute them  which requires the other field so it is created dyanmically 
# here bmi is calculated
