from .database import Base
from sqlalchemy import  Column, Integer, String , Boolean , ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column( Integer, primary_key=True , nullable=False)
    title = Column( String(30) , nullable=False)
    content = Column( String , nullable=False)
    published = Column( Boolean , server_default= 'TRUE' , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE")  , nullable=False)
    files =  Column(String , nullable=True )

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column( Integer, primary_key=True , nullable=False)
    email = Column( String,unique=True , nullable=False)
    password = Column( String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))

