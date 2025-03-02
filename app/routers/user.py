from fastapi import  status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models , schemas , utils 

router = APIRouter(prefix="/api/users" ,
                   tags=["Users"])

@router.post('/' , status_code= status.HTTP_201_CREATED , response_model=schemas.UserOut )
async def create_user(user: schemas.User, db : Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}' , response_model=schemas.UserOut)
async def get_user(id:int , db : Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.id == id).first()
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='User does not exist.')
