# Security Policy

## 🔒 Security Overview

This document outlines security considerations, best practices, and policies for the Inventory Management System backend.

## 🚨 Current Security Status

**Security Level:** ⚠️ DEVELOPMENT ONLY - NOT PRODUCTION READY

### Critical Security Issues

The application currently has the following security vulnerabilities that **MUST** be addressed before production deployment:

1. ❌ Hardcoded secret key in version control
2. ❌ No authentication or authorization
3. ❌ Permissive API access (AllowAny)
4. ❌ Missing CORS configuration
5. ❌ No rate limiting
6. ❌ DEBUG mode enabled

## 🛡️ Security Best Practices

### 1. Secret Management

#### Current Issue
```python
# ❌ BAD - Hardcoded secret
SECRET_KEY = 'django-insecure-dn&wn=b79h1__c2^ouux6q=#6@jq-gowu#snrox-yvydkw_y69'
```

#### Recommended Solution
```python
# ✅ GOOD - Environment variable
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])
```

#### Generate Secure Secret Key
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### Environment File (.env)
```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Important:** Add `.env` to `.gitignore`!

---

### 2. Authentication & Authorization

#### Current Issue
```python
# ❌ BAD - No authentication required
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
```

#### Recommended Solution

**Option A: Token Authentication (Recommended for APIs)**
```python
# settings.py
INSTALLED_APPS += ['rest_framework.authtoken']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

**Option B: JWT Authentication (For more complex scenarios)**
```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

**Option C: Mixed Permissions (Read public, write authenticated)**
```python
# views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
```

---

### 3. CORS Configuration

#### Current Issue
```python
# ❌ INCOMPLETE - Middleware enabled but no origins configured
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]
# No CORS_ALLOWED_ORIGINS setting!
```

#### Recommended Solution

**Development:**
```python
# settings.py
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Development only!
CORS_ALLOW_CREDENTIALS = True
```

**Production:**
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

---

### 4. Input Validation & Sanitization

#### Current Issue
```python
# ❌ NO VALIDATION - Accepts any data matching field types
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

#### Recommended Solution
```python
# ✅ PROPER VALIDATION
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id', 'created_at']
    
    def validate_price(self, value):
        """Validate price is positive and within range."""
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        if value > 999999.99:
            raise serializers.ValidationError("Price exceeds maximum")
        return value
    
    def validate_sku(self, value):
        """Sanitize and validate SKU."""
        # Remove leading/trailing whitespace
        value = value.strip()
        
        # Check for empty value
        if not value:
            raise serializers.ValidationError("SKU cannot be empty")
        
        # Normalize to uppercase
        value = value.upper()
        
        # Check for invalid characters
        import re
        if not re.match(r'^[A-Z0-9\-_]+$', value):
            raise serializers.ValidationError(
                "SKU can only contain letters, numbers, hyphens, and underscores"
            )
        
        return value
    
    def validate_name(self, value):
        """Validate and sanitize product name."""
        value = value.strip()
        
        if not value:
            raise serializers.ValidationError("Name cannot be empty")
        
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters")
        
        # Prevent potential XSS (though DRF handles this)
        import html
        value = html.escape(value)
        
        return value
    
    def validate_stock(self, value):
        """Validate stock quantity."""
        if value > 1000000:
            raise serializers.ValidationError("Stock exceeds maximum limit")
        return value
```

---

### 5. SQL Injection Prevention

**Status:** ✅ PROTECTED

Django ORM automatically protects against SQL injection by using parameterized queries.

```python
# ✅ SAFE - Django ORM parameterizes automatically
Product.objects.filter(sku=user_input)

# ❌ DANGEROUS - Never use raw SQL with user input
Product.objects.raw(f"SELECT * FROM product WHERE sku = '{user_input}'")

# ✅ SAFE - If you must use raw SQL, use parameters
Product.objects.raw("SELECT * FROM product WHERE sku = %s", [user_input])
```

---

### 6. XSS (Cross-Site Scripting) Prevention

**Status:** ✅ MOSTLY PROTECTED (API-only)

Since this is an API-only application, XSS risk is minimal. However:

```python
# ✅ Sanitize input in serializers
import html

def validate_name(self, value):
    return html.escape(value.strip())
```

**Frontend Responsibility:** The Vue.js frontend must properly escape data when rendering.

---

### 7. CSRF Protection

#### For Session Authentication
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',  # Keep enabled
    # ...
]

# For AJAX requests, include CSRF token
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read CSRF cookie
CSRF_COOKIE_SECURE = True     # Only send over HTTPS (production)
CSRF_COOKIE_SAMESITE = 'Strict'
```

#### For Token/JWT Authentication
```python
# CSRF not needed for token-based auth
# But keep middleware for admin interface
```

---

### 8. Rate Limiting

#### Install Django Rate Limiting
```bash
pip install django-ratelimit
```

#### Apply to Views
```python
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='100/h', method='POST'), name='create')
@method_decorator(ratelimit(key='ip', rate='1000/h', method='GET'), name='list')
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

#### Alternative: Use DRF Throttling
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}
```

---

### 9. HTTPS/TLS

#### Production Settings
```python
# settings.py (Production)

# Force HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Other security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

---

### 10. Database Security

#### Password Validation
```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 10}  # Increase from default 8
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

#### Database Connection Security
```python
# For PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'require',  # Require SSL connection
        },
    }
}
```

---

### 11. Logging & Monitoring

#### Security Event Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

#### Log Security Events
```python
import logging

security_logger = logging.getLogger('django.security')

def perform_create(self, serializer):
    security_logger.info(
        f"Product created by {self.request.user} - "
        f"SKU: {serializer.validated_data.get('sku')}"
    )
    super().perform_create(serializer)
```

---

## 🔍 Security Checklist

### Before Production Deployment

- [ ] SECRET_KEY moved to environment variable
- [ ] New SECRET_KEY generated (never reuse dev key)
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured properly
- [ ] Authentication enabled
- [ ] Authorization/permissions configured
- [ ] CORS properly configured (not allowing all origins)
- [ ] Rate limiting implemented
- [ ] HTTPS/TLS enabled
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] Database using SSL connection
- [ ] Logging configured for security events
- [ ] Run `python manage.py check --deploy`
- [ ] Dependencies updated (pip list --outdated)
- [ ] Security audit completed
- [ ] Sensitive data not in version control
- [ ] .gitignore includes .env, *.log, db.sqlite3

### Run Security Check
```bash
python manage.py check --deploy
```

This command will report security issues in your settings.

---

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email security@yourdomain.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours.

---

## 📚 Security Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [DRF Security](https://www.django-rest-framework.org/topics/security/)
- [Django Security Releases](https://www.djangoproject.com/weblog/)

---

## 🔄 Security Updates

Keep dependencies updated:

```bash
pip list --outdated
pip install --upgrade django djangorestframework
```

Subscribe to security mailing lists:
- [Django Security](https://groups.google.com/g/django-announce)
- [Python Security](https://www.python.org/news/security/)

---

**Last Updated:** January 2026  
**Security Policy Version:** 1.0

