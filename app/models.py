from pydantic import BaseModel


# MODELS
class User(BaseModel):
    username: str
    role: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: str
