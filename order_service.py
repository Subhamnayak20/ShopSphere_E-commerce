from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from models import ProductModel
from schemas import ProductCreate, ProductResponse
from deps import get_db


app = FastAPI(title="Order Service")


