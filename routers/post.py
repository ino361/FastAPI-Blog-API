from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session, joinedload
import models, schema
from database import get_db
from oauth2 import get_current_user
from fastapi import UploadFile, File, Form, HTTPException, Depends
import os
import uuid
import shutil
from typing import List, Annotated
from pydantic import WithJsonSchema


router = APIRouter()
SwaggerUploadFile = Annotated[UploadFile, WithJsonSchema({"type": "string", "format": "binary"})]

@router.post('/posts/',response_model=schema.PostResponse)
async def create_post(
    db: Session=Depends(get_db), 
    current_user:models.Users=Depends(get_current_user),
    title: str = Form(None),
    is_published: bool = Form(True),
    images: List[SwaggerUploadFile] = File([]),   
    content: str = Form(None)
    ):

    if len(images) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='En fazla 5 resim yükeyebilirsin'
        )
    
    valid_images = [img for img in images if img.filename !='']
    if not title and not content and len(valid_images) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Boş bişe yapaman'
        )
    
    new_post = models.Post(
        title = title,
        content = content,
        is_published = is_published,
        owner_id = current_user.id
        
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    for img in valid_images:
        file_extension = os.path.splitext(img.filename)[1]
        unique_filename = f'{uuid.uuid4()}{file_extension}'
        file_path = f'static/posts/{unique_filename}'

        try:
            with open (file_path, 'wb+') as buffer:
             shutil.copyfileobj(img.file, buffer)
        except Exception:
            raise HTTPException(
                status_code=500, 
                detail=f"{img.filename} adli resim kaydedilirken bir hata oluştu."
            )

        new_image = models.PostImages(
            images_path = file_path,
            post_id = new_post.id

        )
        db.add(new_image)

    db.commit()
    db.refresh(new_post)
    return new_post




@router.get('/posts', response_model=list[schema.PostResponse])
def get_all_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).options(joinedload(models.Post.comments)).all()
    return posts


@router.delete('/post/{id}',status_code=204,)
def delete_post(id:int, db:Session=Depends(get_db),current_user: models.Users = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail='Post bulunamadi')
    
    if post.images:
        for img in post.images:
            if img.images_path and os.path.exists(img.images_path):
                try:
                    os.remove(img.images_path)
                except Exception as e:
                    print(f'Resim silinirken hata oluştu: {e}')

    if post.comments:
        for comment in post.comments:
            if comment.image_path and os.path.exists(comment.image_path):
                try:
                    os.remove(comment.image_path)

                except Exception as e:
                    print(f'REsim silinirken hata oluştu: {e}')


    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code = 204)


@router.put('/post/{id}',response_model=schema.PostResponse)
def update_post  (
    id:int, 
    updated_post:schema.PostCreate, 
    db:Session=Depends(get_db),
    current_user: models.Users = Depends(get_current_user)
    ):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=404, detail='Post Bulunamadi')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Yetkin yok')
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()



@router.post('/comment/{post_id}', response_model=schema.CommentOut)
async def comment(
    post_id :int,
    text: str = Form(None),
    image: UploadFile = File(None),
    db:Session = Depends(get_db),
    current_user:models.Users = Depends(get_current_user)
):
    post= db.query(models.Post).filter(models.Post.id == post_id ).first()

    if not post:
        raise HTTPException(status_code=404 , detail='Böyle bir post yok')
    
    new_comment = models.Comments(
        text = text,
        owner_id = current_user.id,
        post_id = post_id,
    )

    if image:

        file_extension = os.path.splitext(image.filename)[1]

        unique_filename = f'{uuid.uuid4()}{file_extension}'
        file_path = f'static/comments/{unique_filename}'
        
        try:
            with open(file_path, 'wb+') as buffer:
                shutil.copyfileobj(image.file,buffer)
                
        except Exception:
            raise HTTPException(status_code=500, detail='Resim kaydedilirken hata oluştu')
        
        new_comment.image_path = file_path


    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get('/post/{post_id}',response_model=schema.PostResponse)
def get_one_post(   
    post_id: int, 
    current_user: models.Users = Depends(get_current_user),
    db:Session = Depends(get_db),
    
):    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404 , detail='Post Bulunamadi')
    
    read = db.query(models.Read).filter(
        models.Read.post_id == post_id,
        models.Read.user_id == current_user.id).first()
    if not read:
        new_read =models.Read(
            user_id = current_user.id,
            post_id = post_id,
            
        )
        db.add(new_read)
        db.commit()
        
    return post


@router.get('/{id}')
def post_data(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_user)

):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404 , detail= 'Post Bulunamadi')
    
    already_read = db.query(models.Read).filter(models.Read.post_id == id, models.Read.user_id == current_user.id).first()

    if not already_read:

        new_read = models.Read(
            user_id = current_user.id,
            post_id = id,
           
        )
        db.add(new_read)
        db.commit()
        return post



    