# ShopSphere E-commerce

A microservices-based e-commerce application built with Python and FastAPI, featuring user authentication, product management, and order processing capabilities.

## Overview

ShopSphere is a scalable e-commerce platform that demonstrates modern microservices architecture. The application consists of three independent services that communicate via REST APIs, with support for both Redis and in-memory data storage.

## Architecture

The application follows a microservices architecture with three core services:

- **User Service** (Port 8001): Handles user registration, authentication, and JWT token generation
- **Product Service** (Port 8000): Manages product catalog, inventory, and product queries
- **Order Service** (Port 8002): Processes orders and validates product availability

## Features

### User Service
- User registration with encrypted password storage (bcrypt)
- User login with JWT token authentication
- Secure password hashing and verification
- Email-based user identification

### Product Service
- Create and manage products
- Track product inventory (name, price, quantity)
- Retrieve all products or individual products by ID
- Search products by name

### Order Service
- Place orders with product validation
- Check product availability before order placement
- Track order status (PLACED by default)
- Inter-service communication with Product Service
- View all orders or individual orders by ID

## Technology Stack

- **Framework**: FastAPI
- **Server**: Uvicorn (ASGI server)
- **Database**: Redis (with in-memory fallback)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: Passlib with bcrypt
- **Data Validation**: Pydantic
- **ORM**: Redis-OM (Redis Object Mapper)
- **HTTP Client**: Requests

## Database Support

The application supports two storage modes:

1. **Redis Mode** (Default): Uses Redis with redis-om for persistent data storage
2. **In-Memory Mode**: Fallback mode using a custom in-memory database implementation when Redis is unavailable

Toggle between modes using the `USE_REDIS` environment variable.

## Installation

### Prerequisites
- Python 3.8+
- Redis Server (optional, for Redis mode)
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ShopSphere_E-commerce
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
# Redis Configuration
USE_REDIS=true
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# JWT Configuration
JWT_SECRET=supersecret
```

## Running the Application

### Option 1: Start All Services (Windows PowerShell)
```powershell
.\start_all_services.ps1
```

This script automatically:
- Checks and installs dependencies
- Starts all three services
- Displays service URLs with Swagger documentation

### Option 2: Start Services Individually

**Product Service:**
```bash
uvicorn product_service:app --reload --host 127.0.0.1 --port 8000
```

**User Service:**
```bash
uvicorn user_service:app --reload --host 127.0.0.1 --port 8001
```

**Order Service:**
```bash
uvicorn order_service:app --reload --host 127.0.0.1 --port 8002
```

## API Documentation

Once services are running, access interactive API documentation:

- **Product Service**: http://localhost:8000/docs
- **User Service**: http://localhost:8001/docs
- **Order Service**: http://localhost:8002/docs

## API Endpoints

### User Service (Port 8001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |
| GET | `/` | Health check |

### Product Service (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products` | Create a new product |
| GET | `/products` | Get all products |
| GET | `/products/{pk}` | Get product by ID |
| GET | `/products/search?name=` | Search products by name |
| GET | `/` | Health check |

### Order Service (Port 8002)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/order` | Place a new order |
| GET | `/orders` | Get all orders |
| GET | `/orders/{pk}` | Get order by ID |
| GET | `/` | Health check |

## Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

### Login
```bash
curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

### Create a Product
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99, "quantity": 10}'
```

### Place an Order
```bash
curl -X POST http://localhost:8002/order \
  -H "Content-Type: application/json" \
  -d '{"product_id": "abc123", "quantity": 2}'
```

## Project Structure

```
ShopSphere_E-commerce/
├── user_service.py           # User authentication service
├── product_service.py        # Product management service
├── order_service.py          # Order processing service
├── redis_db.py              # Redis connection configuration
├── in_memory_db.py          # In-memory database fallback
├── requirements.txt         # Python dependencies
├── start_all_services.ps1   # PowerShell startup script
├── test_connection.py       # Connection testing utility
└── README.md               # Project documentation
```

## Security Features

- Password encryption using bcrypt hashing algorithm
- JWT-based authentication for secure API access
- CORS middleware enabled for cross-origin requests
- Environment variable support for sensitive configuration

## Error Handling

The application includes comprehensive error handling:
- 400: Bad Request (invalid data, insufficient quantity)
- 401: Unauthorized (invalid credentials)
- 404: Not Found (user/product/order not found)
- 503: Service Unavailable (inter-service communication failure)

## Development

### In-Memory Mode
For development without Redis, the application automatically falls back to in-memory storage. Set `USE_REDIS=false` or ensure Redis is not available.

### Hot Reload
All services support hot reload during development using the `--reload` flag with uvicorn.

## Internship Project

This project was developed as part of the **Zalimma Internship** program for Python Developer role, demonstrating:
- Microservices architecture design
- RESTful API development
- Database integration (Redis and in-memory)
- Authentication and authorization
- Inter-service communication
- Error handling and validation

## License

This project is part of an internship program at Zalimma.

## Contributing

This is an internship project. For questions or suggestions, please contact the development team.
