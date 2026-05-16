from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
import models, oauth2
from database import get_db

router = APIRouter(
    prefix='/like',
    tags=['Like']
)

@router.post('/{post_id}', status_code=status.HTTP_201_CREATED)

def like_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail='Post bulunamadi')
    
    if post in current_user.liked_posts:
        
        current_user.liked_posts.remove(post)
        db.commit()

        return {'status':'🤍',
                'is_liked':False
        }
    else:

        current_user.liked_posts.append(post)
        db.commit()

        if post.owner_id != current_user.id:
            yeni_bildirim = models.Notification(
                receiver_id=post.owner_id,
                sender_id=current_user.id,
                message=f"{current_user.username} senin postunu begendi.",
                post_id=post.id
            )
            db.add(yeni_bildirim)
            db.commit()
            
        return {'status':'❤️',
                'is_liked':True
        }


@router.get('/',status_code=status.HTTP_200_OK)

def get_liked_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    return current_user.liked_posts