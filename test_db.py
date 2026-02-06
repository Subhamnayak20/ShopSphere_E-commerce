from database import engine
from models import ProductModel as Product

# Create tables
Product.metadata.create_all(bind=engine)

print("✅ Tables created successfully")
