from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
import models, schema, utils
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/register', response_model=schema.UserCreate)
def register(user: schema.UserCreate, db: Session=Depends(get_db)):
    db_user = db.query(models.Users).filter(models.Users.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu kullanici adi mevcut")


    new_user = models.Users(
        username = user.username,
        password = user.password,
        mail = user.mail,
        is_admin = False

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.post('/login',response_model=schema.TokenModel)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db:Session=(Depends(get_db))):
    user = db.query(models.Users).filter(models.Users.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Kullanici adi veya sifre hatali')
    
    
    if user_credentials.password != user.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Kullanici adi veya sifre hatali')
    
    access_token = utils.create_access_token(data={
        'user_id':user.id,
        'is_admin':user.is_admin
    })
    return{
        'access_token':access_token,
        'token_type':'bearer'
    }