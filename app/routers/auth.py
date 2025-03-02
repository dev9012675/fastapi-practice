from fastapi import  status , HTTPException , Depends , APIRouter 
from sqlalchemy.orm import Session
from ..database import  get_db
from .. import models , schemas , utils , oauth2 , config
from fastapi.security import  OAuth2PasswordRequestForm
from dotenv import load_dotenv
from datetime import  timedelta


router = APIRouter(prefix="/api" ,
                   tags=["Authentication"])

@router.post('/login' , response_model=schemas.Token )
async def get_user(user_credentials:OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    user =  db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not utils.verify(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='Invalid Credentials.')
    
    access_token_expires = timedelta(minutes=int(config.settings.access_token_expire_minutes))
    print(f'Access token expiry interval:{access_token_expires}')
    access_token = oauth2.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

    
    

        