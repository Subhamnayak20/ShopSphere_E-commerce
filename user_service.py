from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import datetime
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

class UserSchema(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "User Service is running", "status": "ok"}

@app.post("/register")
def register(user: UserSchema):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users_db[user.email] = {
        "email": user.email,
        "password": pwd_context.hash(user.password)
    }
    
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: LoginRequest):
    if data.email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(data.password, users_db[data.email]["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {"sub": data.email, "iat": datetime.datetime.utcnow().timestamp()}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "token": token}
