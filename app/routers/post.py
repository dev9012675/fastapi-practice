from fastapi import FastAPI , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models , schemas , oauth2
from typing import List 

router = APIRouter(prefix="/api/posts" ,
                   tags=["Posts"])

@router.get("/" , response_model= List[schemas.Post])
async def get_posts(db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user) , limit:int = 10 , skip:int = 0 ,
                       search:str = "" ):
    print(f'The current user is:{current_user.email}')
    #cursor.execute("""SELECT * FROM posts""")
    #post_data = cursor.fetchall()
    #return {"data":post_data}
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/{id}' , response_model=schemas.Post)
async def get_post(id:int , db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""" , [id])
   # post = cursor.fetchone()
    post =  db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    

@router.post('/' , status_code= status.HTTP_201_CREATED , response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts(title , content , published) VALUES(%s , %s , %s) RETURNING *""" ,
    #             (post.title , post.content , post.published))
   # post =  cursor.fetchone()
    #conn.commit()
    new_post = models.Post(owner_id=current_user.id ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{id}' , response_model=schemas.Post)
async def update_post(id:int , post:schemas.PostCreate ,  db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user)):
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()  
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    elif updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='Not authorized to perform action.')
    else:
        update_query.update(post.model_dump() , synchronize_session=False)
        db.commit()
        return update_query.first()
        

@router.delete('/{id}' , status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id:int ,  db : Session = Depends(get_db) , 
                     current_user = Depends(oauth2.get_current_user)):
   # index =  await find_index(id)
   # if index != None:
   #     posts.pop(index)
    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='Not authorized to perform action.')
    else:
        post_query.delete()
        db.commit()