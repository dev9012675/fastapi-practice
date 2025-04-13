from .database import Base
from sqlalchemy import  Column, Integer, String , Boolean , ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class MyBase(Base):
    __abstract__ = True
    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

class Post(MyBase):
    __tablename__ = "posts"
    id = Column( Integer, primary_key=True , nullable=False)
    title = Column( String(30) , nullable=False)
    content = Column( String , nullable=False)
    published = Column( Boolean , server_default= 'TRUE' , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE")  , nullable=False)
    files =  Column(String , nullable=True )

    owner = relationship("User")

class User(MyBase):
    __tablename__ = "users"
    id = Column( Integer, primary_key=True , nullable=False)
    email = Column( String,unique=True , nullable=False)
    password = Column( String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))

