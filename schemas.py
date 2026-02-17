# from pydantic import BaseModel

# class ProductCreate(BaseModel):
#     name: str
#     description: str
#     price: float
#     quantity: int


# class ProductResponse(ProductCreate):
#     id: int

#     class Config:
#         from_attributes = True   # ✅ Pydantic v2


from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]

    class Config:
        from_attributes = True