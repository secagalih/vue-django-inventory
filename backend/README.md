# Inventory Management System - Backend

A RESTful API backend for inventory management built with Django and Django REST Framework.

## 🚀 Quick Start

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
echo "DEBUG=True" >> .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

**Access Points:**
- API: http://localhost:8000/api/products/
- Admin: http://localhost:8000/admin/

## 📚 Documentation

Complete documentation is available in the [`documentation/`](documentation/) folder:

| Document | Description |
|----------|-------------|
| **[Documentation Index](documentation/DOCUMENTATION_INDEX.md)** | Start here - Complete navigation guide |
| **[Quick Start Guide](documentation/QUICKSTART.md)** | 5-minute setup guide |
| **[Complete README](documentation/README.md)** | Comprehensive project documentation |
| **[API Reference](documentation/API.md)** | Complete API documentation with examples |
| **[Architecture Guide](documentation/ARCHITECTURE.md)** | System design and architecture |
| **[Development Guide](documentation/DEVELOPMENT.md)** | Developer workflow and standards |
| **[Code Review](documentation/CODE_REVIEW.md)** | Code quality assessment and recommendations |
| **[Security Policy](documentation/SECURITY.md)** | Security guidelines and best practices |

## 🎯 Key Features

- RESTful API with full CRUD operations
- UUID-based primary keys
- Django Admin interface
- CORS support for frontend integration
- SQLite database (development)

## ⚠️ Important Notes

**This is a development setup.** Before production deployment:

1. ✅ Read [Security Policy](documentation/SECURITY.md)
2. ✅ Review [Code Review](documentation/CODE_REVIEW.md) findings
3. ✅ Fix critical security issues (authentication, secret key, etc.)
4. ✅ Run `python manage.py check --deploy`

## 🛠️ Technology Stack

- **Django** 6.0
- **Django REST Framework** 3.16.1
- **Python** 3.14+
- **SQLite** (development)

## 📖 Quick Links

- [API Endpoints](documentation/API.md#-api-endpoints-overview)
- [Security Checklist](documentation/SECURITY.md#-security-checklist)
- [Development Setup](documentation/DEVELOPMENT.md#-getting-started)
- [Code Standards](documentation/DEVELOPMENT.md#-code-standards)

## 🆘 Need Help?

1. Check [Quick Start Guide](documentation/QUICKSTART.md)
2. Review [Documentation Index](documentation/DOCUMENTATION_INDEX.md)
3. See [Troubleshooting](documentation/QUICKSTART.md#-troubleshooting)

---

**Version:** 1.0.0  
**Last Updated:** January 2026
