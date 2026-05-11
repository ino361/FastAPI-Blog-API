from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models, database, utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Kimlik bilgisi uyusmadi',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    
    user_id = utils.verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user is None:
        raise credentials_exception
    
    return user