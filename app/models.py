from pydantic import BaseModel


# MODELS
class User(BaseModel):
    username: str
    user_type: str


class UserCreate(BaseModel):
    username: str
    name:str
    password: str
    user_type: str
    designation:str
    ticket_no:str
    ward:str
    place_of_posting:str
    
