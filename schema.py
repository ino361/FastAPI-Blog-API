from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = True
    
    


class PostCreate(PostBase):
    pass

class PostImageResponse(BaseModel):
    id: int
    images_path: str


    class Config():
        from_attributes = True


class CommentOut(BaseModel):
    id:int
    text: Optional[str] = None
    owner_id: int
    post_id: int
    image_path: str

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    comments:  list[CommentOut] =[] 
    images: list[PostImageResponse] = []

    class Config:
        from_attributes = True
    

class PostUpdate(PostBase):
    title: Optional [str] = None
    content:Optional [str]= None
    is_published: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class AdminLogin(BaseModel):
    username: str
    password: str

class TokenModel(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str
    password: str
    mail: str
    

class UserResponse(BaseModel):
    username: str
    mail: str
    is_admin: bool
    id: int

    class Config():
        from_attributes = True


class CommentCreate(BaseModel):
    text: str


