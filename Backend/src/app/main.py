from beanie import init_beanie
from fastapi import FastAPI
from app.models import User
from .routers import users, notes
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from .database import database

app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (in development - be specific in production!)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

async def init_db():
    print("Initializing Beanie...")  
    print("Database object:", database)  
    await init_beanie(database, document_models=[User])  # ✅ Ensure correct database object

@app.on_event("startup")
async def startup():
    await init_db()
    
@app.get("/")
async def read_root():
    return {"message": "FastAPI is running"}


app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Notes API"}