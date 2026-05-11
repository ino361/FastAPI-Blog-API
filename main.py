from fastapi import FastAPI, Request, Depends
import models, database
import routers.auth as auth
import routers.post as post
import routers.user as user
from fastapi.responses import JSONResponse
import time
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from fastapi.staticfiles import StaticFiles
import os

models.Base.metadata.create_all(bind=database.engine)


tags_metadata = [
    {
        "name": "Selam Aleyk",        
    }
    ,
    {
        "name": "Authentication",        
    }
    ,
    {
        "name": "Post",        
    }
    ,
    {
        "name": "User",        
    }
]


app = FastAPI(openapi_tags=tags_metadata)

os.makedirs('static/posts', exist_ok=True,)
os.makedirs('static/comments', exist_ok=True,)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(post.router, prefix="/posts", tags=["Post"])
app.include_router(user.router, prefix="/users", tags=["User"])



@app.get('/', tags=['Selam Aleyk'])
def home(
    
    db:Session = Depends (get_db),
    current_user: models.Users = Depends (get_current_user)


):
    read_list = db.query(models.Read.post_id).filter(models.Read.user_id == current_user.id).subquery()

    post = db.query(models.Post).filter(~models.Post.id.in_(read_list)).all()

    return post


login_attempts = {}
BAN_SURESI = 10
MAX_DENEME = 3

@app.middleware('http')
async def  middleware(request: Request, call_next):
    
    client_ip = request.client.host
    current_time = time.time()

    if client_ip in login_attempts:
        user_data = login_attempts[client_ip]


        if user_data['count'] >= MAX_DENEME:
            if current_time < user_data['block_until']:
                kalan_sure = int(user_data['block_until'] - current_time)

                return JSONResponse(
                    status_code=429,
                    content=f'Çok fazla deneme, {kalan_sure} saniye kaldi'
                )
            else:
                login_attempts[client_ip] = {'count': 0, 'block_until': 0}

    response = await call_next(request)

    

    if request.url.path == '/auth/login' and response.status_code == 403:
        data = login_attempts.get(client_ip, {'count': 0, 'block_until':0})
        data['count'] += 1

        if data['count'] >= MAX_DENEME:
            data['block_until'] = current_time + BAN_SURESI
            print ('ip banlandi')

        login_attempts[client_ip] = data
        print(f'Hata sayisi: {data['count']}')

    return response