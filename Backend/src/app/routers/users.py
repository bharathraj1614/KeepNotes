from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, auth
from datetime import timedelta

router = APIRouter()

@router.post("/token")  # MongoDB (Beanie)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await models.User.find_one(models.User.user_email == form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user_email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=schemas.User)  # MongoDB (Beanie)
async def create_user(user: schemas.UserCreate):
    print("User model fields:", models.User.model_fields)
    print("Searching for:", user.user_email)
    db_user = await models.User.find_one({"user_email": user.user_email})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    user_data = user.model_dump(exclude={"password"})
    db_user = models.User(**user_data, password=hashed_password)
    await db_user.insert()
    return db_user


@router.get("/users/me", response_model=schemas.User)  # MongoDB (Beanie)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user