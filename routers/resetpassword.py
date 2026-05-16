import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from git import List
from sqlalchemy.orm import Session
import oauth2
import models, schema
from database import get_db
from datetime import datetime


router = APIRouter(
    prefix='/reset-password',
    tags=['Reset Password']
)


@router.post('/forgot_password')
def forgot_password(request: schema.PasswordResetRequest, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.mail == request.mail).first()
    if not user:
        raise HTTPException(status_code=404, detail='Kullanici bulunamadi')
    
    reset_token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)

    db.token = models.PasswordResetToken(
        user_id=user.id,
        token=reset_token,
        expires_at=expires_at
    )
    db.add(db.token)
    db.commit()

    print(f"\n Link: http://127.0.0.1:8000/auth/reset-password?token={reset_token} \n") #Test amaçlı


    

    # Burada mail gönderme işlemi yapılacak (send_email fonksiyonu ile)
    # send_email(user.mail, reset_token)

    return {
        "status": "✉️",
        "message": "Yeni token bu",
        "test_token": reset_token
    }


@router.post('/reset_password')
def reset_password(request: schema.PasswordResetConfirm, db: Session = Depends(get_db)):

    token_kayit = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == request.token).first()
    if not token_kayit:
        raise HTTPException(status_code=400, detail='Geçersiz token')
    
    if token_kayit.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail='Token süresi dolmuş')
    
    if token_kayit.is_used:
        raise HTTPException(status_code=400, detail='Token Kullanılmış')
    
    user = db.query(models.Users).filter(models.Users.id == token_kayit.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='Kullanici bulunamadi')
    
    user.password = request.new_password
    token_kayit.is_read = True
    token_kayit.is_used = True

    
    db.commit()

    return {
        "status": "✅",
        "message": "Şifre başariyla sifirlandi."
    }



@router.get('/admin/tokens', response_model=List[schema.ResetTokenResponse])
def get_all_reset_tokens(
    db: Session = Depends(get_db), 
    current_user: models.Users = Depends(oauth2.get_current_user)
):
    
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Bu işlem için admin yetkiniz bulunmuyor.")
    
    
    tokens = db.query(models.PasswordResetToken).order_by(models.PasswordResetToken.created_at.desc()).all()
    return tokens