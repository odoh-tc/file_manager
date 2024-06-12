import os
from datetime import datetime
from typing import List
from fastapi import UploadFile, HTTPException, Query
from sqlalchemy.orm import Session
from models.file import File
from models.user import User
from schemas.file import FileUpdate, FileShare, FileAnalytics

UPLOAD_DIRECTORY = "uploads"
ALLOWED_FILE_TYPES = {
    "image/jpeg", "image/png", "video/mp4", "application/pdf",
    "image/gif", "video/x-msvideo", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.ms-powerpoint", "text/plain", "text/csv"
}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def save_upload_file(upload_file: UploadFile, destination: str) -> None:
    with open(destination, "wb") as buffer:
        buffer.write(upload_file.file.read())


def upload_file_service(user_id, file: UploadFile, db: Session):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the limit")

    file.file.seek(0)

    save_upload_file(file, file_location)

    file_size = os.path.getsize(file_location)

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_file = File(
        filename=file.filename,
        file_path=file_location,
        upload_date=datetime.now(),
        file_size=file_size,
        file_type=file.content_type,
        user_id=user_id
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file


def list_user_files_service(user_id: int, db: Session, limit: int = 10, offset: int = 0, search: str = None) -> List[File]:
    query = db.query(File).filter(File.user_id == user_id)
    if search:
        query = query.filter(File.filename.ilike(f"%{search}%"))
    files = query.offset(offset).limit(limit).all()
    return files


def list_all_files_service(db: Session, limit: int = 10, offset: int = 0, search: str = None) -> List[File]:
    query = db.query(File)
    if search:
        query = query.filter(File.filename.ilike(f"%{search}%"))
    files = query.offset(offset).limit(limit).all()
    return files


def get_file_service(file_id: int, user_id: int, db: Session) -> File:
    file = db.query(File).filter(File.id == file_id, File.user_id == user_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


def update_file_service(file_id: int, user_id: int, file_update: FileUpdate, db: Session) -> File:
    file = db.query(File).filter(File.id == file_id, File.user_id == user_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    old_file_path = file.file_path

    if file_update.filename:
        # Ensure the new filename includes the extension
        old_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{file_update.filename}{old_extension}"
        new_file_path = os.path.join("uploads", new_filename)

        # Update the filename and file path in the database
        file.filename = new_filename
        file.file_path = new_file_path

        # Update the filename in the filesystem
        if os.path.exists(old_file_path):
            try:
                os.rename(old_file_path, new_file_path)
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Original file not found on disk")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error renaming file: {e}")
        else:
            raise HTTPException(status_code=404, detail="Original file not found on disk")

    db.commit()
    db.refresh(file)
    return file


def delete_file_service(file_id: int, user_id: int, db: Session) -> File:
    file = db.query(File).filter(File.id == file_id, File.user_id == user_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = file.file_path
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="File not found on disk")

    db.delete(file)
    db.commit()
    return file


def share_file_link_service(file_id: int, user_id: int, db: Session, base_url: str) -> FileShare:
    file = db.query(File).filter(File.id == file_id, File.user_id == user_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    share_link = f"{base_url}/file/shared/{file_id}"
    return FileShare(file_id=file.id, share_link=share_link)


def download_file_service(file_id: int, db: Session) -> File:
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


def get_file_analytics_service(user_id: int, db: Session) -> FileAnalytics:
    files = db.query(File).filter(File.user_id == user_id).all()
    total_size = sum(file.file_size for file in files)
    total_size_with_unit = total_size
    if total_size < 1024:
        size_unit = "B"
    elif total_size < 1024 ** 2:
        total_size_with_unit = total_size / 1024
        size_unit = "KB"
    elif total_size < 1024 ** 3:
        total_size_with_unit = total_size / (1024 ** 2)
        size_unit = "MB"
    else:
        total_size_with_unit = total_size / (1024 ** 3)
        size_unit = "GB"
    analytics = FileAnalytics(total_files=len(files), total_size=total_size, total_size_with_unit=total_size_with_unit,
                              size_unit=size_unit)
    return analytics
