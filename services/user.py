from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.user import UserCreate, UserUpdate, UserIn
from utils.password_utils import get_password_hash
from models.user import User
from fastapi import HTTPException
from typing import List, Optional

# Function to check if user exists
def check_user_exists(db: Session, username: str, email: str) -> bool:
    return db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first() is not None

# Function to create a new user
def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to register a new user
def register_new_user(db: Session, user: UserCreate):
    if check_user_exists(db, user.username, user.email):
        raise HTTPException(status_code=400, detail="Username or email already exists.")
    return create_user(db, user)

# Function to update user details
def update_user(db: Session, current_user: User, user_update: UserUpdate) -> User:
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    if user_update.password:
        current_user.password = user_update.password  # Hash the password in a real application
    db.commit()
    db.refresh(current_user)
    return current_user

# Function to fetch all users with pagination and search
def fetch_all_users(db: Session, limit: int, offset: int, search: Optional[str] = None) -> List[User]:
    query = db.query(User)
    if search:
        query = query.filter(func.lower(User.username).contains(search.lower()) | func.lower(User.email).contains(search.lower()))
    return query.offset(offset).limit(limit).all()

# Function to fetch a user by ID
def fetch_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Function to delete a user by ID
def delete_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
