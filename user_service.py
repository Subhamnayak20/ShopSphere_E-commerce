import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

USE_REDIS = os.getenv("USE_REDIS", "true").lower() == "true"

if USE_REDIS:
    try:
        from redis_om import HashModel
        from redis_db import redis
    except Exception:
        USE_REDIS = False

from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import datetime

from in_memory_db import InMemoryModel

app = FastAPI(title="User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

if USE_REDIS:
    class User(HashModel):
        email: str
        password: str

        class Meta:
            database = redis
else:
    class User(InMemoryModel):
        def __init__(self, email: str, password: str):
            super().__init__(email=email, password=password)


# --------------------
# Request Body Schema
# --------------------
class LoginRequest(BaseModel):
    email: str
    password: str

class UserSchema(BaseModel):
    email: str
    password: str

# --------------------
# Register API
# --------------------
@app.post("/register")
def register(user: UserSchema):
    if USE_REDIS:
        existing = User.find(User.email == user.email).all()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        u = User(email=user.email, password=pwd_context.hash(user.password))
        u.save()
    else:
        existing = User.find_by("email", user.email).all()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        u = User(email=user.email, password=pwd_context.hash(user.password))
        u.save()
    return {"message": "User registered successfully"}

# --------------------
# Login API
# --------------------
@app.post("/login")
def login(data: LoginRequest):
    if USE_REDIS:
        users = User.find(User.email == data.email).all()
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        user = users[0]
        hashed = user.password
    else:
        users = User.find_by("email", data.email).all()
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        user_dict = users[0]
        hashed = user_dict.get("password")

    if not pwd_context.verify(data.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {"sub": data.email, "iat": datetime.datetime.utcnow().timestamp()}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "token": token}

@app.get("/")
def root():
    return {"message": "User Service is running"}
