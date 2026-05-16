from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schema, oauth2
from database import get_db

router = APIRouter(
    prefix='/notifications',
    tags=['Notifications']
)


@router.get('/', response_model=List[schema.NotificationResponse])
def get_notifications(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), unread_only: bool = False):

    notifications = db.query(models.Notification).filter(models.Notification.receiver_id == current_user.id)

    if unread_only:
        notifications = notifications.filter(models.Notification.is_read == False) #Okunmamislar gözüksün

    notifications = notifications.order_by(models.Notification.created_at.desc()).all() # Okunmamıslar en üstte görüksün
    return notifications




@router.put('/{notification_id}/read', status_code=status.HTTP_200_OK)
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    notification = db.query(models.Notification).filter(models.Notification.id == notification_id, models.Notification.receiver_id == current_user.id).first()

    if not notification:
        raise HTTPException(status_code=404, detail='Bildirim bulunamadi')
    
    notification.is_read = True
    db.commit()

    return {'status': '✅', 'message': 'Okundu'}