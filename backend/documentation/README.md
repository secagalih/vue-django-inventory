# Inventory Management System - Backend

A RESTful API backend for inventory management built with Django and Django REST Framework.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)

## 🎯 Overview

This backend application provides a RESTful API for managing product inventory. It enables CRUD operations for products, including tracking product names, SKUs, pricing, and stock levels.

### Key Capabilities

- Full CRUD operations for product management
- RESTful API design following industry standards
- UUID-based primary keys for distributed system compatibility
- Django Admin interface for manual data management
- CORS support for frontend integration

## ✨ Features

### Current Features

- **Product Management**
  - Create, Read, Update, Delete products
  - Unique SKU (Stock Keeping Unit) tracking
  - Price management with decimal precision
  - Stock quantity tracking
  - Automatic timestamp recording (created_at)

- **API**
  - RESTful endpoints with standard HTTP methods
  - JSON request/response format
  - Automatic API endpoint generation via DRF Router
  - CORS enabled for frontend communication

- **Admin Interface**
  - Django Admin panel for product management
  - User-friendly interface at `/admin/`

## 🛠 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Django | 6.0 |
| **API Framework** | Django REST Framework | 3.16.1 |
| **Database** | SQLite | 3.x (dev) |
| **CORS** | django-cors-headers | 4.9.0 |
| **Config Management** | python-decouple | 3.8 |
| **Language** | Python | 3.14 |

## 📁 Project Structure

```
backend/
├── inventory_project/          # Django project configuration
│   ├── __init__.py
│   ├── settings.py            # Project settings and configuration
│   ├── urls.py                # Main URL routing
│   ├── wsgi.py                # WSGI application entry point
│   └── asgi.py                # ASGI application entry point
│
├── inventory/                  # Main inventory application
│   ├── migrations/            # Database migrations
│   │   └── 0001_initial.py   # Initial Product model
│   ├── __init__.py
│   ├── admin.py              # Admin interface registration
│   ├── apps.py               # App configuration
│   ├── models.py             # Product data model
│   ├── serializers.py        # DRF serializers for JSON conversion
│   ├── views.py              # API view logic (ViewSets)
│   ├── urls.py               # App-specific URL routing
│   └── tests.py              # Test cases (to be implemented)
│
├── manage.py                  # Django management script
├── db.sqlite3                 # SQLite database file
├── venv/                      # Python virtual environment
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.14 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework django-cors-headers python-decouple
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the backend directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/
```

### Endpoints

#### Products

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products/` | List all products | No |
| POST | `/api/products/` | Create a new product | No* |
| GET | `/api/products/{id}/` | Retrieve a specific product | No |
| PUT | `/api/products/{id}/` | Full update of a product | No* |
| PATCH | `/api/products/{id}/` | Partial update of a product | No* |
| DELETE | `/api/products/{id}/` | Delete a product | No* |

*Note: Authentication is currently disabled. It's recommended to enable authentication before production deployment.

### Product Model

```json
{
  "id": "uuid",
  "name": "string (max 100 chars)",
  "sku": "string (max 50 chars, unique)",
  "price": "decimal (10 digits, 2 decimal places)",
  "stock": "integer (non-negative)",
  "created_at": "datetime (auto-generated)"
}
```

### Example Requests

**Create a Product:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "sku": "LAP-001",
    "price": "999.99",
    "stock": 15
  }'
```

**Get All Products:**
```bash
curl http://localhost:8000/api/products/
```

**Get Single Product:**
```bash
curl http://localhost:8000/api/products/{product-uuid}/
```

**Update Product:**
```bash
curl -X PATCH http://localhost:8000/api/products/{product-uuid}/ \
  -H "Content-Type: application/json" \
  -d '{
    "stock": 20
  }'
```

**Delete Product:**
```bash
curl -X DELETE http://localhost:8000/api/products/{product-uuid}/
```

## 🔧 Development

### Running the Development Server

```bash
python manage.py runserver
```

Access points:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Making Model Changes

1. Modify models in `inventory/models.py`
2. Create migrations:
   ```bash
   python manage.py makemigrations
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

### Django Shell

Access the Django shell for debugging and data manipulation:
```bash
python manage.py shell
```

Example:
```python
from inventory.models import Product

# Create a product
product = Product.objects.create(
    name="Test Product",
    sku="TEST-001",
    price=49.99,
    stock=10
)

# Query products
Product.objects.all()
Product.objects.filter(stock__gt=5)
```

## 🧪 Testing

Run tests:
```bash
python manage.py test
```

Run tests with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔒 Security Considerations

### Current State (Development)

⚠️ **The following settings are FOR DEVELOPMENT ONLY:**

- `DEBUG = True`
- `AllowAny` permissions on API
- Hardcoded SECRET_KEY (should be in environment variables)
- CORS configured to allow all origins

### Before Production

1. **Environment Variables**
   - Move SECRET_KEY to environment variables
   - Set DEBUG=False
   - Configure ALLOWED_HOSTS

2. **Authentication & Authorization**
   - Implement user authentication
   - Add permission classes to ViewSets
   - Consider JWT tokens for stateless auth

3. **CORS Configuration**
   - Restrict CORS to specific domains
   - Remove `CORS_ALLOW_ALL_ORIGINS`

4. **Database**
   - Migrate from SQLite to PostgreSQL/MySQL
   - Set up database backups
   - Use connection pooling

5. **HTTPS**
   - Enforce HTTPS in production
   - Set secure cookie flags
   - Configure HSTS headers

## 🚀 Deployment

### Checklist

- [ ] Set environment variables
- [ ] Change database to production-grade (PostgreSQL)
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up static file serving
- [ ] Configure CORS for production domains
- [ ] Enable authentication/authorization
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Run security checks: `python manage.py check --deploy`

### Deployment Options

- **Platform as a Service**: Heroku, Railway, Render
- **Container-based**: Docker + Kubernetes
- **Traditional**: Gunicorn + Nginx on VPS
- **Serverless**: AWS Lambda + API Gateway

## 📝 Configuration Reference

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db

# CORS (for production)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Settings Overview

| Setting | Purpose | Current Value | Production Value |
|---------|---------|---------------|------------------|
| DEBUG | Enable debug mode | True | False |
| ALLOWED_HOSTS | Allowed host headers | [] | ['yourdomain.com'] |
| SECRET_KEY | Cryptographic signing | Hardcoded | From env var |
| DATABASES | Database config | SQLite | PostgreSQL |
| CORS_ALLOW_ALL_ORIGINS | CORS policy | True | False |

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'rest_framework'`**
```bash
pip install djangorestframework
```

**Issue: Database not found**
```bash
python manage.py migrate
```

**Issue: Port 8000 already in use**
```bash
python manage.py runserver 8001
```

**Issue: CORS errors from frontend**
- Ensure `corsheaders` is in INSTALLED_APPS
- Verify CORS middleware is properly positioned
- Check CORS configuration in settings.py

## 📞 Support

For issues and questions:
- Check the [Django documentation](https://docs.djangoproject.com/)
- Review [DRF documentation](https://www.django-rest-framework.org/)
- Create an issue in the project repository

---

**Version:** 1.0.0  
**Last Updated:** January 2026

