from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import User, Note 

MONGO_DETAILS = "mongodb://localhost:27017/KeepApp"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["KeepApp"]

async def init_db():
    await init_beanie(database=database, document_models=[User, Note])
