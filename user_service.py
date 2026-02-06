from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
import datetime
import os

try:
    import redis
    redis_conn = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )
    redis_conn.ping()
    USE_REDIS = True
except Exception as e:
    print(f"Redis connection failed: {e}. Using in-memory storage.")
    USE_REDIS = False
    users_db = {}

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
    if USE_REDIS:
        existing = redis_conn.hgetall(f"user:{user.email}")
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        
        hashed_password = pwd_context.hash(user.password)
        redis_conn.hset(f"user:{user.email}", mapping={
            "email": user.email,
            "password": hashed_password
        })
    else:
        if user.email in users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        
        users_db[user.email] = {
            "email": user.email,
            "password": pwd_context.hash(user.password)
        }
    
    return {"message": "User registered successfully"}

@app.post("/login")
def login(data: LoginRequest):
    if USE_REDIS:
        user_data = redis_conn.hgetall(f"user:{data.email}")
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not pwd_context.verify(data.password, user_data["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        if data.email not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not pwd_context.verify(data.password, users_db[data.email]["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_data = {"sub": data.email, "iat": datetime.datetime.utcnow().timestamp()}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"message": "Login successful", "token": token}
