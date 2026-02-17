from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import bcrypt
from jose import jwt
from datetime import datetime, timezone
import os

# In-memory database
users_db = {}

app = FastAPI(title="User Service")

# CORS Configuration - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = None  # Not using passlib
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class UserSchema(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepass123"
            }
        }

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "User Service is running", "status": "ok"}

@app.post("/register")
def register(user: UserSchema):
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    users_db[user.email] = {
        "email": user.email,
        "password": hash_password(user.password)
    }
    
    return {"message": "User registered successfully", "email": user.email}

@app.post("/login")
def login(data: LoginRequest):
    if data.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(data.password, users_db[data.email]["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {"sub": data.email, "iat": datetime.now(timezone.utc).timestamp()}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "token": token}
