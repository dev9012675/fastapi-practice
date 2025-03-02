from fastapi import  status , HTTPException , Depends , APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import models , schemas , oauth2

router = APIRouter(prefix="/api/vote" ,
                   tags=["Vote"])

@router.post('/' , status_code=status.HTTP_201_CREATED)
def vote_post(vote:schemas.Vote , db : Session = Depends(get_db) , 
                      current_user = Depends(oauth2.get_current_user)):
    post =  db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
        

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , 
                 models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , 
                                detail=f'User with id {current_user.id} has already liked the post with id {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id , user_id = current_user.id )
        db.add(new_vote)
        db.commit()
        return {"message":"Post liked successfully"}
        
        
    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , 
                                detail=f'User with id {current_user.id} has not liked the post  with id {vote.post_id}')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Like removed successfully"}

