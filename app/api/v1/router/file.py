import os
from typing import List
from fastapi import APIRouter, Depends, Query, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.file import FileDeleteResponse, FileSchema, FileUpdate, FileShare, FileAnalytics
from services.file import ( delete_file_service, get_file_analytics_service, get_file_service, list_all_files_service, 
                           share_file_link_service, upload_file_service,
                             list_user_files_service, download_file_service,
                            update_file_service )
from ..dependencies.auth import get_current_active_admin, get_current_user
from models.user import User
from core.config import settings

__all__ = [
    "upload_file",
    "list_user_files",
    "list_all_files",
    "get_file_analytics",
    "get_file",
    "update_file",
    "delete_file",
    "share_file_link",
    "download_file"
]

router = APIRouter()


@router.post("/upload", response_model=FileSchema)
async def upload_file(
    file: UploadFile = UploadFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileSchema:
    """
    Upload a new file.

    Parameters:
    - file (UploadFile): The file to be uploaded.
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileSchema: The uploaded file with its metadata.
    """
    db_file = upload_file_service(current_user.id, file, db)
    return db_file


@router.get("/files", response_model=List[FileSchema])
async def list_user_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str = Query(None, description="Search term to filter files by filename")
) -> List[FileSchema]:
    """
    List all files belonging to the current user.

    Parameters:
    - db (Session): A database session.
    - current_user (User): The current user making the request.
    - limit (int): The maximum number of files to return.
    - offset (int): The index of the first file to return.
    - search (str): A search term to filter files by filename.

    Returns:
    - List[FileSchema]: A list of files belonging to the current user.
    """
    files = list_user_files_service(current_user.id, db, limit=limit, offset=offset, search=search)
    return files


# Admin-specific endpoint
@router.get("/admin", response_model=List[FileSchema])
async def list_all_files(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_admin),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: str = Query(None, description="Search term to filter files by filename")
) -> List[FileSchema]:
    """
    List all files in the system.

    Parameters:
    - db (Session): A database session.
    - current_admin (User): The current admin making the request.
    - limit (int): The maximum number of files to return.
    - offset (int): The index of the first file to return.
    - search (str): A search term to filter files by filename.

    Returns:
    - List[FileSchema]: A list of all files in the system.
    """
    files = list_all_files_service(db, limit=limit, offset=offset, search=search)
    return files



@router.get("/analytics", response_model=FileAnalytics)
async def get_file_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileAnalytics:
    """
    Get file analytics for the current user.

    Parameters:
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileAnalytics: File analytics data for the current user.
    """
    analytics = get_file_analytics_service(current_user.id, db)
    return {
        "total_files": analytics.total_files,
        "total_size": analytics.total_size,
        "size_unit": analytics.total_size_with_unit
    }



@router.get("/{file_id}", response_model=FileSchema)
async def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileSchema:
    """
    Get a specific file by its ID.

    Parameters:
    - file_id (int): The ID of the file to retrieve.
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileSchema: The specific file with its metadata.
    """
    file = get_file_service(file_id, current_user.id, db)
    return file



@router.put("/{file_id}", response_model=FileSchema)
async def update_file(
    file_id: int,
    file_update: FileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileSchema:
    """
    Update a specific file by its ID.

    Parameters:
    - file_id (int): The ID of the file to update.
    - file_update (FileUpdate): The updated metadata for the file.
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileSchema: The updated file with its metadata.
    """
    updated_file = update_file_service(file_id, current_user.id, file_update, db)
    return updated_file



@router.delete("/{file_id}", response_model=FileDeleteResponse)
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileDeleteResponse:
    """
    Delete a specific file by its ID.

    Parameters:
    - file_id (int): The ID of the file to delete.
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileDeleteResponse: A message confirming the deletion of the file.
    """
    deleted_file = delete_file_service(file_id, current_user.id, db)
    return {
        "message": f"File '{deleted_file.filename}' has been successfully deleted.",
        "file": deleted_file
    }



@router.post("/{file_id}/share", response_model=FileShare)
async def share_file_link(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> FileShare:
    """
    Generate a shareable link for a specific file by its ID.

    Parameters:
    - file_id (int): The ID of the file to generate a shareable link for.
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileShare: A dictionary containing the shareable link and the file metadata.
    """
    # Use the base URL from your settings or environment
    base_url = settings.BASE_URL  
    share_link = share_file_link_service(file_id, current_user.id, db, base_url)
    return share_link



@router.get("/shared/{file_id}")
async def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Enforce authentication
) -> FileResponse:
    """
    Download a specific file by its ID.

    Parameters:
    - file_id (int): The ID of the file to download.
    - db (Session): A database session.
    - current_user (User): The current user making the request.

    Returns:
    - FileResponse: A response containing the file data.
    """
    file = download_file_service(file_id, db)
    file_path = file.file_path

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=file.filename)