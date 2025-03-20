from beanie import Document
from datetime import datetime
import uuid
import beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
from typing import Optional

from beanie import Document
MONGO_DETAILS = "mongodb://localhost:27017/KeepApp"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.get_default_database()

class User(Document):
    id: Optional[uuid.UUID] = None  
    user_name: str
    user_email: str  
    password: str
    create_on: datetime = datetime.utcnow()  

    class Settings:
        collection = "users" 


class Note(Document):
    user_id: uuid.UUID
    note_title: str
    note_content: str
    last_update: datetime = Field(default_factory=datetime.utcnow)  
    create_on: datetime = Field(default_factory=datetime.utcnow)  

    class Settings:
        collection = "notes"

    class Config:
        collection = "notes"

async def init_db():
    await beanie.init_odm(database=db, document_models=[User, Note]) 