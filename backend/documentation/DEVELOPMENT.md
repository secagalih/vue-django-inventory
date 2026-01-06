# Development Guide

Complete guide for developers working on the Inventory Management System backend.

## 📚 Table of Contents

- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Database Management](#database-management)
- [Testing](#testing)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.14+**
- **pip** (Python package manager)
- **Git**
- **Virtual Environment** (venv)

Verify installations:

```bash
python --version    # Should show 3.14+
pip --version
git --version
```

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vue-django-inventory/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # macOS/Linux:
   source venv/bin/activate
   
   # Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   
   # If requirements.txt doesn't exist, install manually:
   pip install django djangorestframework django-cors-headers python-decouple
   ```

5. **Create .env file**
   ```bash
   # Create .env in the backend directory
   touch .env
   ```
   
   Add the following content:
   ```env
   SECRET_KEY=your-secret-key-here-change-in-production
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

Visit:
- API: http://localhost:8000/api/products/
- Admin: http://localhost:8000/admin/

## 🔧 Development Environment Setup

### Recommended IDE Setup

#### VS Code Extensions

- **Python** (Microsoft)
- **Django** (Baptiste Darthenay)
- **Pylance** (Microsoft)
- **Python Test Explorer**
- **REST Client** (Huachao Mao)

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.rulers": [88],
    "editor.tabSize": 4
  }
}
```

### Install Development Tools

```bash
# Code formatting
pip install black isort

# Linting
pip install flake8 pylint

# Testing
pip install pytest pytest-django pytest-cov

# Type checking
pip install mypy django-stubs djangorestframework-stubs
```

### Pre-commit Hooks (Optional but Recommended)

```bash
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.14
  
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']
EOF

# Install the hooks
pre-commit install
```

## 📁 Project Structure

```
backend/
├── inventory_project/          # Project configuration
│   ├── __init__.py
│   ├── settings.py            # ⚙️ Main settings
│   ├── urls.py                # 🔗 Main URL routing
│   ├── wsgi.py                # 🌐 WSGI config
│   └── asgi.py                # 🌐 ASGI config
│
├── inventory/                  # Main app
│   ├── migrations/            # 📊 Database migrations
│   ├── __init__.py
│   ├── admin.py              # 🔧 Admin configuration
│   ├── apps.py               # ⚙️ App configuration
│   ├── models.py             # 📋 Data models
│   ├── serializers.py        # 🔄 DRF serializers
│   ├── views.py              # 👁️ API views
│   ├── urls.py               # 🔗 App URLs
│   └── tests.py              # 🧪 Tests
│
├── manage.py                  # Django CLI
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
└── README.md                  # Documentation
```

## 🔄 Development Workflow

### Standard Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Edit code
   - Add/modify models
   - Update tests

3. **Run tests**
   ```bash
   python manage.py test
   ```

4. **Format code**
   ```bash
   black .
   isort .
   ```

5. **Commit changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Making Model Changes

1. **Edit model** in `inventory/models.py`
   ```python
   class Product(models.Model):
       # ... existing fields ...
       updated_at = models.DateTimeField(auto_now=True)  # New field
   ```

2. **Create migration**
   ```bash
   python manage.py makemigrations
   ```

3. **Review migration file**
   ```bash
   cat inventory/migrations/0002_product_updated_at.py
   ```

4. **Apply migration**
   ```bash
   python manage.py migrate
   ```

5. **Test the change**
   ```bash
   python manage.py shell
   >>> from inventory.models import Product
   >>> p = Product.objects.first()
   >>> print(p.updated_at)
   ```

### Adding New API Endpoints

1. **Define custom action in ViewSet**
   ```python
   # inventory/views.py
   from rest_framework.decorators import action
   from rest_framework.response import Response
   
   class ProductViewSet(ModelViewSet):
       # ... existing code ...
       
       @action(detail=True, methods=['post'])
       def adjust_stock(self, request, pk=None):
           product = self.get_object()
           adjustment = request.data.get('adjustment', 0)
           product.stock += adjustment
           product.save()
           return Response(self.get_serializer(product).data)
   ```

2. **Test the endpoint**
   ```bash
   curl -X POST http://localhost:8000/api/products/{id}/adjust_stock/ \
     -H "Content-Type: application/json" \
     -d '{"adjustment": 10}'
   ```

## 📏 Code Standards

### Python Style Guide

Follow **PEP 8** with these specific rules:

- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Single quotes preferred
- **Imports**: Organized by isort

### Import Order

```python
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
from django.db import models
from rest_framework import serializers

# Local imports
from .models import Product
from .utils import helper_function
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Class | PascalCase | `ProductSerializer` |
| Function | snake_case | `get_product_list` |
| Variable | snake_case | `product_count` |
| Constant | UPPER_SNAKE_CASE | `MAX_PRICE` |
| Model | PascalCase | `Product` |

### Docstrings

Use Google-style docstrings:

```python
def calculate_total_value(products):
    """Calculate total inventory value.
    
    Args:
        products (QuerySet): Product queryset to calculate value for.
    
    Returns:
        Decimal: Total value of all products.
    
    Example:
        >>> products = Product.objects.all()
        >>> total = calculate_total_value(products)
        >>> print(total)
        Decimal('12345.67')
    """
    return sum(p.price * p.stock for p in products)
```

### Type Hints

Add type hints for better code clarity:

```python
from typing import List, Optional
from decimal import Decimal

def get_products_below_price(max_price: Decimal) -> List[Product]:
    """Get products below a certain price."""
    return Product.objects.filter(price__lt=max_price)

def find_product_by_sku(sku: str) -> Optional[Product]:
    """Find product by SKU, return None if not found."""
    try:
        return Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        return None
```

## 🗄️ Database Management

### Common Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback migration
python manage.py migrate inventory 0001

# Create empty migration (for data migrations)
python manage.py makemigrations --empty inventory

# SQL for migration (without applying)
python manage.py sqlmigrate inventory 0001
```

### Django Shell

```bash
python manage.py shell
```

```python
# Common queries
from inventory.models import Product

# Create
product = Product.objects.create(
    name='Test Product',
    sku='TEST-001',
    price=19.99,
    stock=100
)

# Read
products = Product.objects.all()
product = Product.objects.get(sku='TEST-001')
products = Product.objects.filter(stock__gt=10)

# Update
product.stock = 150
product.save()

# Delete
product.delete()

# Bulk operations
Product.objects.filter(stock=0).update(stock=10)
Product.objects.filter(stock__lt=0).delete()

# Aggregation
from django.db.models import Sum, Avg, Count
total_stock = Product.objects.aggregate(Sum('stock'))
avg_price = Product.objects.aggregate(Avg('price'))
product_count = Product.objects.aggregate(Count('id'))
```

### Database Backup & Restore

```bash
# Backup (SQLite)
cp db.sqlite3 db.sqlite3.backup

# Restore (SQLite)
cp db.sqlite3.backup db.sqlite3

# Export data as JSON
python manage.py dumpdata inventory.Product > products.json

# Import data from JSON
python manage.py loaddata products.json
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test inventory

# Run specific test class
python manage.py test inventory.tests.ProductTestCase

# Run specific test method
python manage.py test inventory.tests.ProductTestCase.test_create_product

# Run with verbosity
python manage.py test --verbosity 2

# Keep database after tests (for debugging)
python manage.py test --keepdb
```

### Writing Tests

```python
# inventory/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Product

class ProductAPITestCase(APITestCase):
    
    def setUp(self):
        """Run before each test method."""
        self.product = Product.objects.create(
            name='Test Product',
            sku='TEST-001',
            price=Decimal('99.99'),
            stock=10
        )
        self.url = '/api/products/'
    
    def test_list_products(self):
        """Test listing all products."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_product(self):
        """Test creating a new product."""
        data = {
            'name': 'New Product',
            'sku': 'NEW-001',
            'price': '49.99',
            'stock': 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
    
    def test_duplicate_sku_fails(self):
        """Test that duplicate SKU is rejected."""
        data = {
            'name': 'Duplicate',
            'sku': 'TEST-001',  # Already exists
            'price': '29.99',
            'stock': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def tearDown(self):
        """Run after each test method."""
        Product.objects.all().delete()
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run --source='.' manage.py test

# Generate report
coverage report

# Generate HTML report
coverage html
# Open htmlcov/index.html in browser
```

## 🐛 Debugging

### Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# urls.py
import debug_toolbar
urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

### Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'inventory': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
```

### Using Python Debugger

```python
# In your code
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

## 🔧 Common Tasks

### Create Requirements File

```bash
pip freeze > requirements.txt
```

### Reset Database

```bash
# Delete database
rm db.sqlite3

# Delete migrations (keep __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recreate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Add Sample Data

```python
# Create seed_data.py
from inventory.models import Product

products = [
    {'name': 'Laptop', 'sku': 'LAP-001', 'price': 999.99, 'stock': 10},
    {'name': 'Mouse', 'sku': 'MOU-001', 'price': 29.99, 'stock': 50},
    {'name': 'Keyboard', 'sku': 'KEY-001', 'price': 79.99, 'stock': 30},
]

for p in products:
    Product.objects.create(**p)
```

```bash
python manage.py shell < seed_data.py
```

## 🔍 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'rest_framework'`**
```bash
pip install djangorestframework
```

**Issue: Port 8000 already in use**
```bash
# Use different port
python manage.py runserver 8001

# Or kill the process
lsof -ti:8000 | xargs kill -9
```

**Issue: Migration conflicts**
```bash
python manage.py migrate --fake inventory zero
python manage.py migrate inventory
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic
```

---

**Last Updated:** January 2026  
**Maintained By:** Development Team

