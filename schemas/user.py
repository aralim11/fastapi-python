from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class CurrentUser(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True