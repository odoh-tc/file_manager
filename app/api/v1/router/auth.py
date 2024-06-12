from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.session import get_db
from schemas.auth import Token
from services.auth import create_access_token
from models.user import User
from datetime import timedelta
from core.config import settings
from schemas.user import UserCreate, UserRole
from services.user import register_new_user
from fastapi import status

from utils.password_utils import verify_password

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user in the database.

    Args:
    - user (UserCreate): A dictionary containing the user's data.
    - db (Session, optional): A database session. Defaults to Depends(get_db).

    Returns:
    - User: The newly created user object.

    Raises:
    - HTTPException: If an HTTP exception occurs during user registration.
    """
    try:
        created_user = register_new_user(db, user)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return created_user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Logs in a user and returns an access token.

    Args:
    - form_data (OAuth2PasswordRequestForm): A dictionary containing the user's login credentials.
    - db (Session, optional): A database session. Defaults to Depends(get_db).

    Returns:
    - dict: A dictionary containing the access token and token type.

    Raises:
    - HTTPException: If the username or password is incorrect.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value},  # Include role in token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}