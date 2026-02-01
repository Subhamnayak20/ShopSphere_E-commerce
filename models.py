from sqlalchemy import Column, Integer, String, Float
from database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)

    