from fastapi import  status , HTTPException , Depends , APIRouter , Form
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models , schemas , oauth2 , utils
from typing import List , Annotated 

router = APIRouter(prefix="/api/posts" ,
                   tags=["Posts"])

@router.get("/" , response_model= List[schemas.Post])
async def get_posts(db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user) , limit:int = 10 , skip:int = 0 ,
                       search:str = "" ):
    print(f'The current user is:{current_user.email}')
    posts = db.query(models.Post).all()
    return posts


@router.get('/{id}' , response_model=schemas.Post)
async def get_post(id:int , db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user)):

    post =  db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    

@router.post('/' , status_code= status.HTTP_201_CREATED )
async def create_post(post: Annotated[schemas.PostCreate , Form()], db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user)):
    postDict = post.model_dump()
    audioFiles = postDict.pop('audioFiles')
    new_post = models.Post(owner_id=current_user.id ,**postDict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    if  audioFiles:
        path = f'files/{current_user.id}/posts/{new_post.id}/'
        for file in audioFiles:
            await utils.create_file( path , file)
        update_query = db.query(models.Post).filter(models.Post.id == new_post.id)
        update_query.update({"files":path} , synchronize_session=False)
        db.commit()
        new_post = update_query.first()
    else:
        print('Post has no audio files')
    
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
    post_query =  db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    elif post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='Not authorized to perform action.')
    else:
        post_query.delete()
        db.commit()