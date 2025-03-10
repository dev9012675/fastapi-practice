from pydantic import BaseModel , EmailStr , Field
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content : str 
    published: Optional[bool] = None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    class Config:
        orm_mode = True

class User(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str
    email:EmailStr
    id:int

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id:int
    dir:int = Field(le= 1)