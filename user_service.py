from fastapi import FastAPI
from redis_om import HashModel
from redis_db import redis
from pydantic import BaseModel

app = FastAPI(title="User Service")


class User(HashModel):
    email: str
    password: str

    class Meta:
        database = redis


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/register")
def register(user: User):
    user.save()
    return {"message": "User registered successfully"}


@app.post("/login")
def login(data: LoginRequest):
    users = User.find(User.email == data.email).all()

    if not users:
        return {"error": "User not found"}

    if users[0].password != data.password:
        return {"error": "Invalid credentials"}

    return {
        "message": "Login successful",
        "token": "mock-token"
    }

@app.get("/")
def root():
    return {"message": "User Service is running"}
