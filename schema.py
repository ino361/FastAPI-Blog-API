from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = True
    



    
class NotificationResponse(BaseModel): #Bildirimler için dönen şema
    receiver_id: int
    message: str
    sender_id: int
    id: int
    created_at: datetime
    is_read: bool
    post_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserFollowListResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PostSimpleResponse(BaseModel):#Like ve Takip için dönen şema
    id: int
    username: str

    class Config:
        from_attributes = True



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
    estimated_read_time: Optional[int] = None

    class Config:
        from_attributes = True


class PostDetailResponse(PostResponse):
    liked_by_users: list[str] = []
    

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



class ResetTokenResponse(BaseModel):
    token: str
    created_at: datetime
    expires_at: datetime
    id: int
    user_id: int
    is_used: bool

    class Config:
        from_attributes = True




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

class PasswordResetRequest(BaseModel):
    mail: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
