from sqlalchemy import Column, ForeignKey, Integer, String, Float
from database import Base

class ProductModel(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)

class OrderModel(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    product_id = Column("product_id", ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer)
    total_price = Column(Float)