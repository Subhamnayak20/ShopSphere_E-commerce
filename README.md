# ShopSphere E-commerce

A microservices-based e-commerce application built with Python and FastAPI, featuring user authentication, product management, and order processing capabilities.

## Overview

ShopSphere is a scalable e-commerce platform that demonstrates modern microservices architecture. The application consists of three independent services that communicate via REST APIs, with support for both Redis and in-memory data storage.

## Architecture

The application follows a microservices architecture with three core services:

- **User Service** (Port 8001): Handles user registration, authentication, and JWT token generation
- **Product Service** (Port 8000): Manages product catalog, inventory, and product queries
- **Order Service** (Port 8002): Processes orders and validates product availability

## C4 Model Architecture Diagrams

### Level 1: System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                         ShopSphere                              │
│                    E-commerce Platform                          │
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │    User      │      │   Product    │      │    Order     │ │
│  │   Service    │      │   Service    │      │   Service    │ │
│  │  (Port 8001) │      │ (Port 8000)  │      │ (Port 8002)  │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         ▲                                                ▲
         │                                                │
         │                                                │
    ┌────┴────┐                                     ┌────┴────┐
    │  Web    │                                     │ Mobile  │
    │ Client  │                                     │  App    │
    └─────────┘                                     └─────────┘
```

### Level 2: Container Diagram with API Gateway

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          ShopSphere Platform                               │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │                        API Gateway (Future)                       │    │
│  │                    [Port 8080 - Not Implemented]                  │    │
│  │  • Request Routing                                                │    │
│  │  • Load Balancing                                                 │    │
│  │  • Authentication/Authorization                                   │    │
│  │  • Rate Limiting                                                  │    │
│  └────────┬─────────────────────┬─────────────────────┬─────────────┘    │
│           │                     │                     │                   │
│           │ REST/HTTP           │ REST/HTTP           │ REST/HTTP         │
│           ▼                     ▼                     ▼                   │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐        │
│  │  User Service   │   │ Product Service │   │  Order Service  │        │
│  │   [FastAPI]     │   │    [FastAPI]    │   │    [FastAPI]    │        │
│  │   Port 8001     │   │   Port 8000     │   │   Port 8002     │        │
│  │                 │   │                 │   │                 │        │
│  │ • Registration  │   │ • CRUD Products │   │ • Place Orders  │        │
│  │ • Login/JWT     │   │ • Inventory Mgmt│   │ • Order Status  │        │
│  │ • Auth          │   │ • Search        │   │ • Validation    │        │
│  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘        │
│           │                     │                     │                   │
│           │                     │                     │ REST API          │
│           │                     │                     │ (requests lib)    │
│           │                     │◄────────────────────┘                   │
│           │                     │  GET /products/{id}                     │
│           │                     │  (Product Validation)                   │
│           ▼                     ▼                     ▼                   │
│  ┌─────────────────────────────────────────────────────────────┐        │
│  │                    Data Storage Layer                        │        │
│  │                                                               │        │
│  │  ┌──────────────┐              ┌──────────────┐             │        │
│  │  │    Redis     │              │  In-Memory   │             │        │
│  │  │   Database   │      OR      │   Database   │             │        │
│  │  │ (redis-om)   │              │   (Fallback) │             │        │
│  │  └──────────────┘              └──────────────┘             │        │
│  └───────────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────────────────────────┘
```

### Level 3: Component Diagram - Inter-Service Communication

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Inter-Service Communication Flow                     │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐                                          ┌──────────────┐
│   Client     │                                          │   Client     │
│ Application  │                                          │ Application  │
└──────┬───────┘                                          └──────┬───────┘
       │                                                         │
       │ 1. POST /register                                       │
       │    {email, password}                                    │
       ▼                                                         │
┌─────────────────┐                                             │
│  User Service   │                                             │
│   Port 8001     │                                             │
│                 │                                             │
│  ┌───────────┐  │                                             │
│  │  Auth     │  │                                             │
│  │ Component │  │                                             │
│  │           │  │                                             │
│  │ • bcrypt  │  │                                             │
│  │ • JWT     │  │                                             │
│  └───────────┘  │                                             │
└─────────────────┘                                             │
                                                                │
       2. POST /login                                           │
          Returns: JWT Token                                    │
                                                                │
                                                                │
                                                                │ 3. POST /products
                                                                │    {name, price, qty}
                                                                ▼
                                                         ┌─────────────────┐
                                                         │ Product Service │
                                                         │   Port 8000     │
                                                         │                 │
                                                         │  ┌───────────┐  │
                                                         │  │ Inventory │  │
                                                         │  │ Component │  │
                                                         │  │           │  │
                                                         │  │ • CRUD    │  │
                                                         │  │ • Search  │  │
                                                         │  └───────────┘  │
                                                         └────────┬────────┘
                                                                  │
       ┌──────────────────────────────────────────────────────────┘
       │
       │ 4. Order Placement Flow
       │
┌──────┴───────┐
│   Client     │
│ Application  │
└──────┬───────┘
       │
       │ 5. POST /order
       │    {product_id, quantity}
       ▼
┌─────────────────┐          REST API Call (HTTP)          ┌─────────────────┐
│  Order Service  │────────────────────────────────────────>│ Product Service │
│   Port 8002     │  GET /products/{product_id}            │   Port 8000     │
│                 │                                         │                 │
│  ┌───────────┐  │  6. Validate Product Availability      │  ┌───────────┐  │
│  │  Order    │  │     • Check product exists             │  │ Inventory │  │
│  │Processing │  │     • Verify quantity                  │  │ Component │  │
│  │ Component │  │                                         │  └───────────┘  │
│  │           │  │<────────────────────────────────────────│                 │
│  │ • Create  │  │  Returns: Product Details              │                 │
│  │ • Validate│  │  {id, name, price, quantity}           │                 │
│  └───────────┘  │                                         └─────────────────┘
│                 │
│  7. Create Order│
│     if valid    │
└─────────────────┘
```

### Level 4: Communication Protocols & Patterns

#### Current Implementation: REST/HTTP

```
┌─────────────────────────────────────────────────────────────────┐
│                    REST API Communication                       │
└─────────────────────────────────────────────────────────────────┘

Order Service ──────────────────────> Product Service
                REST/HTTP
                
  Protocol: HTTP/1.1
  Method: GET
  Endpoint: http://localhost:8000/products/{product_id}
  Headers: 
    - Content-Type: application/json
  Response Format: JSON
  Library: Python requests
  
  Flow:
  1. Order Service receives order request
  2. Makes synchronous HTTP GET to Product Service
  3. Validates product exists and has sufficient quantity
  4. Creates order if validation passes
  5. Returns order confirmation or error

  Error Handling:
  • 404: Product not found
  • 400: Insufficient quantity
  • 503: Product Service unavailable
```

#### Future Enhancement: gRPC (Recommended)

```
┌─────────────────────────────────────────────────────────────────┐
│                    gRPC Communication (Future)                  │
└─────────────────────────────────────────────────────────────────┘

Order Service ══════════════════════> Product Service
                gRPC/HTTP2
                
  Protocol: HTTP/2
  Method: RPC Call
  Service: ProductService.GetProduct()
  Message Format: Protocol Buffers
  
  Benefits:
  • Faster serialization (Protocol Buffers vs JSON)
  • Bi-directional streaming support
  • Built-in code generation
  • Better performance for inter-service calls
  • Type-safe contracts
  
  Proto Definition Example:
  
  service ProductService {
    rpc GetProduct(ProductRequest) returns (ProductResponse);
    rpc CheckAvailability(AvailabilityRequest) returns (AvailabilityResponse);
  }
```

### Communication Matrix

| Source Service | Target Service | Protocol | Endpoint | Purpose |
|----------------|----------------|----------|----------|----------|
| Client | User Service | REST/HTTP | POST /register | User registration |
| Client | User Service | REST/HTTP | POST /login | Authentication |
| Client | Product Service | REST/HTTP | POST /products | Create product |
| Client | Product Service | REST/HTTP | GET /products | List products |
| Client | Product Service | REST/HTTP | GET /products/{id} | Get product details |
| Client | Order Service | REST/HTTP | POST /order | Place order |
| Client | Order Service | REST/HTTP | GET /orders | List orders |
| **Order Service** | **Product Service** | **REST/HTTP** | **GET /products/{id}** | **Validate product** |

### Data Flow Sequence

```
Complete Order Placement Flow:

┌────────┐      ┌──────────┐      ┌─────────────┐      ┌─────────────┐
│ Client │      │   User   │      │   Order     │      │   Product   │
│        │      │ Service  │      │  Service    │      │   Service   │
└───┬────┘      └────┬─────┘      └──────┬──────┘      └──────┬──────┘
    │                │                    │                    │
    │ 1. Register    │                    │                    │
    │───────────────>│                    │                    │
    │                │                    │                    │
    │ 2. Login       │                    │                    │
    │───────────────>│                    │                    │
    │<───────────────│                    │                    │
    │   JWT Token    │                    │                    │
    │                │                    │                    │
    │                │                    │  3. Create Product │
    │────────────────┼────────────────────┼───────────────────>│
    │                │                    │                    │
    │ 4. Place Order │                    │                    │
    │────────────────┼───────────────────>│                    │
    │                │                    │                    │
    │                │                    │ 5. Validate Product│
    │                │                    │───────────────────>│
    │                │                    │<───────────────────│
    │                │                    │  Product Details   │
    │                │                    │                    │
    │                │                    │ 6. Check Quantity  │
    │                │                    │                    │
    │                │                    │ 7. Create Order    │
    │<───────────────┼────────────────────│                    │
    │  Order Confirm │                    │                    │
    │                │                    │                    │
```

### Architecture Patterns

- **Pattern**: Microservices Architecture
- **Communication**: Synchronous REST API calls
- **Service Discovery**: Direct URL configuration (localhost)
- **Data Storage**: Redis (primary) / In-Memory (fallback)
- **Authentication**: JWT-based token authentication
- **API Style**: RESTful HTTP/JSON
- **Error Handling**: HTTP status codes with JSON error responses

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

### Option 1: Kubernetes (Recommended for Production)

**Prerequisites:**
- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl CLI installed
- NGINX Ingress Controller

**Deploy:**
```bash
# Build images
docker build -f Dockerfile.product -t shopsphere/product-service:latest .
docker build -f Dockerfile.user -t shopsphere/user-service:latest .
docker build -f Dockerfile.order -t shopsphere/order-service:latest .

# Deploy to Kubernetes
kubectl apply -f k8s/ -n shopsphere

# Verify
kubectl get pods -n shopsphere
```

**Access:** http://shopsphere.local/api/

See [k8s/README.md](k8s/README.md) for detailed instructions.

### Option 2: Docker Compose with Load Balancing (Recommended for Staging)

**Prerequisites:**
- Docker Desktop installed
- Docker Compose v3.8+

**Start with load balancing (2 instances per service + NGINX):**
```bash
docker-compose -f docker-compose.lb.yml up -d
```

**Access via NGINX Load Balancer:**
- All services: http://localhost/api/
- Product Service: http://localhost/api/products
- User Service: http://localhost/api/users
- Order Service: http://localhost/api/orders

**View logs:**
```bash
docker-compose -f docker-compose.lb.yml logs -f
```

**Stop:**
```bash
docker-compose -f docker-compose.lb.yml down
```

See [LOAD_BALANCING.md](LOAD_BALANCING.md) for detailed configuration.

### Option 3: Docker Compose (Simple)

**Start all services:**
```bash
docker-compose up -d
```

**Service URLs:**
- Product Service: http://localhost:8000/docs
- User Service: http://localhost:8001/docs
- Order Service: http://localhost:8002/docs

**Stop:**
```bash
docker-compose down
```

### Option 4: Start All Services (Windows PowerShell)
```powershell
.\start_all_services.ps1
```

This script automatically:
- Checks and installs dependencies
- Starts all three services
- Displays service URLs with Swagger documentation

### Option 5: Start Services Individually

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
├── docker-compose.yml       # Docker Compose configuration
├── docker-compose.lb.yml    # Docker Compose with load balancing
├── nginx.conf               # NGINX load balancer configuration
├── Dockerfile.user          # User service Docker image
├── Dockerfile.product       # Product service Docker image
├── Dockerfile.order         # Order service Docker image
├── .dockerignore            # Docker ignore patterns
├── k8s/                     # Kubernetes manifests
│   ├── namespace.yaml       # Namespace configuration
│   ├── config.yaml          # ConfigMap and Secrets
│   ├── redis.yaml           # Redis deployment
│   ├── product-service.yaml # Product service deployment
│   ├── user-service.yaml    # User service deployment
│   ├── order-service.yaml   # Order service deployment
│   ├── ingress.yaml         # Ingress configuration
│   ├── hpa.yaml             # Horizontal Pod Autoscaler
│   └── README.md            # Kubernetes deployment guide
├── start_all_services.ps1   # PowerShell startup script
├── test_connection.py       # Connection testing utility
├── test_services.py         # Service validation script
├── LOAD_BALANCING.md        # Load balancing documentation
├── FIXES.md                 # Service fixes documentation
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

This project was developed as part of the **Zaalima Internship** program for Python Developer role, demonstrating:
- Microservices architecture design
- RESTful API development
- Database integration (Redis and in-memory)
- Authentication and authorization
- Inter-service communication
- Error handling and validation
- Docker containerization
- Kubernetes orchestration
- Load balancing and high availability
- Horizontal pod autoscaling

## License

This project is part of an internship program at Zalimma.

## Contributing

This is an internship project. For questions or suggestions, please contact the development team.
