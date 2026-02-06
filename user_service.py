from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel
from redis_db import redis
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import datetime
import os

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

class User(HashModel):
    email: str
    password: str

    class Meta:
        database = redis

class UserSchema(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "User Service is running"}

@app.post("/register")
def register(user: UserSchema):
    existing = User.find(User.email == user.email).all()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    u = User(email=user.email, password=pwd_context.hash(user.password))
    u.save()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: LoginRequest):
    users = User.find(User.email == data.email).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users[0]
    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {"sub": data.email, "iat": datetime.datetime.utcnow().timestamp()}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "token": token}
