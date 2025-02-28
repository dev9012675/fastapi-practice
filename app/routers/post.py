from fastapi import FastAPI , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models , schemas , oauth2
from typing import List 

router = APIRouter(prefix="/api/posts" ,
                   tags=["Posts"])

@router.get("/" , response_model= List[schemas.Post])
async def get_posts(db : Session = Depends(get_db) , 
                      current_user:int = Depends(oauth2.get_current_user)):
    print(f'The current user is:{current_user.email}')
    #cursor.execute("""SELECT * FROM posts""")
    #post_data = cursor.fetchall()
    #return {"data":post_data}
    posts = db.query(models.Post).all()
    return posts


@router.get('/{id}' , response_model=schemas.Post)
async def get_post(id:int , db : Session = Depends(get_db) , 
                      current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""" , [id])
   # post = cursor.fetchone()
    post =  db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    

@router.post('/' , status_code= status.HTTP_201_CREATED , response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db : Session = Depends(get_db) , 
                      current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts(title , content , published) VALUES(%s , %s , %s) RETURNING *""" ,
    #             (post.title , post.content , post.published))
   # post =  cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{id}' , response_model=schemas.Post)
async def update_post(id:int , post:schemas.PostCreate ,  db : Session = Depends(get_db) , 
                      current_user:int = Depends(oauth2.get_current_user)):
    updated_post =  db.query(models.Post).filter(models.Post.id == id)
    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    else:
        updated_post.update(post.model_dump() , synchronize_session=False)
        db.commit()
        return updated_post.first()
        

@router.delete('/{id}' , status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id:int ,  db : Session = Depends(get_db) , 
                     current_user:int = Depends(oauth2.get_current_user)):
   # index =  await find_index(id)
   # if index != None:
   #     posts.pop(index)
    post =  db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    else:
        post.delete()
        db.commit()