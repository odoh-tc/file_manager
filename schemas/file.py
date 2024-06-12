from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FileBase(BaseModel):
    filename: str
    file_path: str
    upload_date: datetime
    file_size: int
    file_type: str

class FileCreate(FileBase):
    pass

class FileSchema(FileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class FileUpdate(BaseModel):
    filename: Optional[str] = None

class FileDeleteResponse(BaseModel):
    message: str
    file: FileSchema


class FileShare(BaseModel):
    file_id: int
    share_link: str

class FileAnalytics(BaseModel):
    total_files: int
    total_size: int
    size_unit: str

    @property
    def total_size_with_unit(self):
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = self.total_size
        for unit in units:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    @classmethod
    def from_db(cls, total_files: int, total_size: int):
        return cls(total_files=total_files, total_size=total_size, size_unit="B")