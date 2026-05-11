from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payload.get("user_id")
        

       
        #expire = payload.get('exp')
        #if expire < int(datetime.timestamp(datetime.utcnow())):
           # print('Buradayim')
            #raise credentials_exception
        
        if user_id is None:
            
            raise credentials_exception
        
        return user_id
    except ExpiredSignatureError:
        print("Hata: Token'ın süresi dolmuş!")
    except JWTError:
        
        raise credentials_exception

