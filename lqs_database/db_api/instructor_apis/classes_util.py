from pydantic import BaseModel
from typing import Union


class Students(BaseModel):
    name: Union[str, None]
    email: Union[str, None]
    
    class Config:
        orm_mode = True
        
        
class genResponce(BaseModel):
    status: bool = False
    message: Union[str, None]
    
    class Config:
        orm_mode = True
        
class ClassInput(BaseModel):
    class_name: str
    course_code: str
    instructor_id: int
    
    class Config:
        orm_mode = True