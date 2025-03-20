from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    user_name: str
    user_email: str
    password: str

class User(UserCreate):
    user_id: str
    last_update: datetime
    create_on: datetime

    class Config:
        orm_mode = True

class NoteCreate(BaseModel):
    note_title: str
    note_content: str

class NoteUpdate(BaseModel):
    note_title: Optional[str] = None
    note_content: Optional[str] = None

class Note(NoteCreate):
    note_id: str
    user_id: str
    last_update: datetime
    created_on: datetime

    class Config:
        orm_mode = True