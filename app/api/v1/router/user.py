from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.user import UserIn, UserUpdate, UserDeleteResponse
from models.user import User
from app.api.v1.dependencies.auth import get_current_user
from services.user import update_user, delete_user_by_id, fetch_user, fetch_all_users
from schemas.user import UserRole
from typing import List, Optional

__all__ = ["users_router"]

router = APIRouter()

# Dependency to check if user is an admin
def admin_only(current_user: User = Depends(get_current_user)):
    """
    Dependency to check if the current user is an admin.

    Args:
        current_user (User): The current user object.

    Returns:
        User: The current user object if they are an admin, else raises an HTTPException.

    Raises:
        HTTPException: If the current user is not an admin.
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only!")
    return current_user

# Route to get user's profile
@router.get("/profile/", response_model=UserIn)
async def read_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Route to get the profile of the current user.

    Args:
        current_user (User): The current user object.
        db (Session): The database session.

    Returns:
        UserIn: The profile of the current user.
    """
    return current_user

# Route to update user's profile
@router.put("/profile/", response_model=UserIn)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Route to update the profile of the current user.

    Args:
        user_update (UserUpdate): The updated user data.
        current_user (User): The current user object.
        db (Session): The database session.

    Returns:
        UserIn: The updated profile of the current user.
    """
    updated_user = update_user(db, current_user, user_update)
    return updated_user

# Route to get all users (admin only) with pagination and search
@router.get("/admin/users/", response_model=List[UserIn])
async def get_all_users(
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None, description="Search term to filter users by username or email")
):
    """
    Route to get all users (admin only) with pagination and search.

    Args:
        current_user (User): The current user object.
        db (Session): The database session.
        limit (int): The maximum number of users to return.
        offset (int): The starting index for the users to return.
        search (Optional[str]): The search term to filter users by username or email.

    Returns:
        List[UserIn]: A list of user profiles matching the search criteria.
    """
    users = fetch_all_users(db, limit=limit, offset=offset, search=search)
    return users

# Route to get a user by ID (admin only)
@router.get("/admin/{user_id}/", response_model=UserIn)
async def get_user(
    user_id: int,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Route to get a user by ID (admin only).

    Args:
        user_id (int): The ID of the user to retrieve.
        current_user (User): The current user object.
        db (Session): The database session.

    Returns:
        UserIn: The profile of the user with the given ID.
    """
    user = fetch_user(db, user_id)
    return user

# Route to delete a user by ID (admin only)
@router.delete("/admin/{user_id}/", response_model=UserDeleteResponse)
async def delete_user(
    user_id: int,
    current_user: User = Depends(admin_only),
    db: Session = Depends(get_db)
):
    """
    Route to delete a user by ID (admin only).

    Args:
        user_id (int): The ID of the user to delete.
        current_user (User): The current user object.
        db (Session): The database session.

    Returns:
        UserDeleteResponse: A dictionary containing the deleted user and a message.
    """
    user = delete_user_by_id(db, user_id)
    return {
        "user": user,
        "message": f"User with id {user_id} has been deleted"
    }