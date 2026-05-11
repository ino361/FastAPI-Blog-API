from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schema
from database import get_db


router = APIRouter()

# @app.get yerine @router.get
@router.get('/users', response_model=list[schema.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Users).all()
    return all_users

@router.get('/users/{id}',response_model=schema.UserResponse)
def select_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id == id)
    users = user_query.first()

    if not users:
        raise HTTPException(status_code=404, detail='Kullanici id bulunamadi')
    return users