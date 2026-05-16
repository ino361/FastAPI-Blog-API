from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, oauth2, schema
from database import get_db

router = APIRouter(
    prefix='/follow',
    tags=['Follow']
)

@router.post('/{user_id}', status_code=status.HTTP_201_CREATED)
def follow_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    user_to_follow = db.query(models.Users).filter(models.Users.id == user_id).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail='Kullanici bulunamadi')
    
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail='Kendini takip edemezsin')

    
    if user_to_follow in current_user.following:
        current_user.following.remove(user_to_follow)
        db.commit()

        return {'status':'❌',
                'is_following':False,
                'status_code':status.HTTP_200_OK
        }
    else:
        current_user.following.append(user_to_follow)
        db.commit()

        yeni_bildirim = models.Notification(
            receiver_id=user_to_follow.id,
            sender_id=current_user.id,
            message=f"{current_user.username} seni takip etmeye basladi."
        )
        db.add(yeni_bildirim)
        db.commit()

        return {'status':'✅',
                'is_following':True
        }
    
@router.get('/followers', response_model=list[schema.UserFollowListResponse])#Takip Edenler
def get_followers(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    followers = current_user.followers
    return followers


@router.get('/following', response_model=list[schema.UserFollowListResponse])#Takip Ettikleri
def get_following(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    following = current_user.following
    return following