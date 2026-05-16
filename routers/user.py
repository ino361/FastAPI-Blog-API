from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
from oauth2 import get_current_user
import oauth2
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



#Admin Check


@router.put('/make-admin/{user_id}')
def make_user_admin(
    user_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    #Admin kontrol
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Yetkin yok"
        )
    
    
    user_to_upgrade = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user_to_upgrade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Kullanici yok"
        )
        
    # Adminse bişi yapma
    if user_to_upgrade.is_admin:
        return {"message": f"{user_to_upgrade.username} zaten admin."}
    
    
    user_to_upgrade.is_admin = True
    db.commit()
    db.refresh(user_to_upgrade)
    
    return {"message": f"{user_to_upgrade.username} sa kardeş"}