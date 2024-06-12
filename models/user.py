from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base import Base
from schemas.user import UserRole  # Import UserRole

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    joined_date = Column(DateTime, nullable=False, default=datetime.now)
    password = Column(String(100), nullable=False)  
    role = Column(Enum(UserRole), default=UserRole.user) 

    files = relationship('File', back_populates='user')