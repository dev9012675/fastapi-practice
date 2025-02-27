from fastapi import FastAPI , status , HTTPException , Depends
from pydantic import BaseModel 
from dotenv import load_dotenv
from typing import Optional
from . import models
from .database import engine , get_db
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title:str
    content : str 
    published: Optional[bool] = None

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts(db : Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #post_data = cursor.fetchall()
    #return {"data":post_data}
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.get('/posts/{id}')
async def get_post(id:int , db : Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""" , [id])
   # post = cursor.fetchone()
    post =  db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return {"data":post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    

@app.post('/posts' , status_code= status.HTTP_201_CREATED)
async def create_post(post: Post, db : Session = Depends(get_db)):
    #cursor.execute(""" INSERT INTO posts(title , content , published) VALUES(%s , %s , %s) RETURNING *""" ,
    #             (post.title , post.content , post.published))
   # post =  cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'data':new_post}

@app.put('/posts/{id}')
async def update_post(id:int , post:Post ,  db : Session = Depends(get_db)):
    updated_post =  db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    else:
        updated_post.update(post.model_dump() , synchronize_session=False)
        db.commit()
        return {"data":updated_post.first()}
        



@app.delete('/posts/{id}' , status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id:int ,  db : Session = Depends(get_db)):
   # index =  await find_index(id)
   # if index != None:
   #     posts.pop(index)
    post =  db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    else:
        post.delete()
        db.commit()





