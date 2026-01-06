# Quick Start Guide

Get the Inventory Management System backend up and running in 5 minutes!

## ⚡ Quick Setup

### 1. Prerequisites Check

```bash
python --version  # Should be 3.14+
pip --version
```

### 2. Clone & Navigate

```bash
cd vue-django-inventory/backend
```

### 3. Create Virtual Environment

```bash
# Create
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration

Create `.env` file:

```bash
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
echo "DEBUG=True" >> .env
echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
```

Or manually create `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Database Setup

```bash
python manage.py migrate
```

### 7. Create Admin User

```bash
python manage.py createsuperuser
# Follow prompts to create username/password
```

### 8. Start Server

```bash
python manage.py runserver
```

## 🎉 You're Ready!

### Access Points

- **API:** http://localhost:8000/api/products/
- **Admin:** http://localhost:8000/admin/

### Quick Test

```bash
# Test API (should return empty array)
curl http://localhost:8000/api/products/

# Create a product
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "sku": "TEST-001",
    "price": "19.99",
    "stock": 10
  }'

# List products again (should show the new product)
curl http://localhost:8000/api/products/
```

## 📖 Next Steps

1. **Read the Documentation**
   - [`README.md`](README.md) - Complete overview
   - [`API.md`](API.md) - API reference
   - [`ARCHITECTURE.md`](ARCHITECTURE.md) - System design
   - [`DEVELOPMENT.md`](DEVELOPMENT.md) - Development guide
   - [`CODE_REVIEW.md`](CODE_REVIEW.md) - Code review findings
   - [`SECURITY.md`](SECURITY.md) - Security guidelines

2. **Add Sample Data**
   ```bash
   python manage.py shell
   ```
   
   ```python
   from inventory.models import Product
   from decimal import Decimal
   
   products = [
       {'name': 'Laptop', 'sku': 'LAP-001', 'price': Decimal('999.99'), 'stock': 10},
       {'name': 'Mouse', 'sku': 'MOU-001', 'price': Decimal('29.99'), 'stock': 50},
       {'name': 'Keyboard', 'sku': 'KEY-001', 'price': Decimal('79.99'), 'stock': 30},
   ]
   
   for p in products:
       Product.objects.create(**p)
   
   exit()
   ```

3. **Explore Admin Interface**
   - Go to http://localhost:8000/admin/
   - Login with your superuser credentials
   - Manage products visually

## 🔧 Common Commands

```bash
# Start server
python manage.py runserver

# Start server on different port
python manage.py runserver 8001

# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Django shell
python manage.py shell

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser
```

## 🐛 Troubleshooting

### Port 8000 already in use?
```bash
python manage.py runserver 8001
```

### Virtual environment not activating?
```bash
# Ensure you're in the backend directory
cd backend

# Try activating again
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Module not found errors?
```bash
# Ensure virtual environment is active
# Then reinstall dependencies
pip install -r requirements.txt
```

### Database errors?
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

## 📚 API Examples

### List All Products
```bash
curl http://localhost:8000/api/products/
```

### Create Product
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "sku": "WM-001",
    "price": "29.99",
    "stock": 150
  }'
```

### Get Single Product
```bash
curl http://localhost:8000/api/products/{product-id}/
```

### Update Product (Partial)
```bash
curl -X PATCH http://localhost:8000/api/products/{product-id}/ \
  -H "Content-Type: application/json" \
  -d '{"stock": 200}'
```

### Delete Product
```bash
curl -X DELETE http://localhost:8000/api/products/{product-id}/
```

## 🚀 Development Workflow

1. **Make changes** to code
2. **Run tests** (when available)
   ```bash
   python manage.py test
   ```
3. **Start server** to test manually
   ```bash
   python manage.py runserver
   ```
4. **Check changes** in browser or with curl

## ⚠️ Important Notes

- This is a **development setup** - do not use in production as-is
- Read [`SECURITY.md`](SECURITY.md) before deploying
- Review [`CODE_REVIEW.md`](CODE_REVIEW.md) for improvement recommendations
- Database is SQLite (suitable for development only)
- Authentication is disabled (see security docs)

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Official Docs](https://docs.python.org/)

---

**Need Help?** Check the detailed documentation in the other markdown files!

