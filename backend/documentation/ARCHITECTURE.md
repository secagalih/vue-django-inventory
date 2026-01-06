# Architecture Documentation

## 🏗️ System Architecture Overview

This document provides an in-depth look at the architectural decisions, design patterns, and structure of the Inventory Management System backend.

## 📐 Architectural Pattern

The application follows the **Model-View-Controller (MVC)** pattern, specifically adapted to Django's MTV (Model-Template-View) architecture, enhanced with Django REST Framework for API capabilities.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                         │
│              (Frontend, Mobile, API Clients)             │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/HTTPS
                        │ JSON
┌───────────────────────▼─────────────────────────────────┐
│                    API Gateway Layer                     │
│                  (Django URL Router)                     │
│              • CORS Middleware                           │
│              • Security Middleware                       │
│              • Authentication Middleware                 │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                 Presentation Layer                       │
│              (ViewSets & Serializers)                    │
│                                                          │
│  ProductViewSet ──────► ProductSerializer                │
│  • List, Create, Update, Delete                          │
│  • Request validation                                    │
│  • Response formatting                                   │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   Business Layer                         │
│              (Models & Business Logic)                   │
│                                                          │
│  Product Model                                           │
│  • Data validation                                       │
│  • Business rules                                        │
│  • Constraints                                           │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                   Data Access Layer                      │
│                  (Django ORM)                            │
│                                                          │
│  • Query optimization                                    │
│  • Transaction management                                │
│  • Database abstraction                                  │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                    Database Layer                        │
│                   (SQLite / PostgreSQL)                  │
│                                                          │
│  Products Table                                          │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Design Principles

### 1. Separation of Concerns

Each component has a single, well-defined responsibility:

- **Models** (`models.py`): Define data structure and business rules
- **Serializers** (`serializers.py`): Handle data transformation and validation
- **ViewSets** (`views.py`): Control request/response flow and orchestration
- **URLs** (`urls.py`): Route requests to appropriate handlers
- **Settings** (`settings.py`): Centralize configuration

### 2. DRY (Don't Repeat Yourself)

- Uses Django's ORM to avoid SQL repetition
- Leverages DRF's `ModelViewSet` for automatic CRUD operations
- Employs `ModelSerializer` for automatic field generation

### 3. Convention Over Configuration

- Follows Django's standard project structure
- Uses DRF's default routing conventions
- Adheres to REST API naming conventions

## 📦 Component Deep Dive

### Data Model Layer

#### Product Model

```python
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Design Decisions:**

1. **UUID Primary Key**
   - **Why**: Globally unique identifiers suitable for distributed systems
   - **Benefit**: No ID conflicts when syncing across systems
   - **Trade-off**: Slightly larger than integer PKs, less human-readable

2. **Unique SKU Constraint**
   - **Why**: SKUs must be unique across the inventory
   - **Benefit**: Database-level guarantee of uniqueness
   - **Implementation**: Database creates a unique index

3. **DecimalField for Price**
   - **Why**: Avoid floating-point precision errors
   - **Benefit**: Exact decimal arithmetic for financial calculations
   - **Configuration**: 10 total digits, 2 decimal places (max: 99,999,999.99)

4. **PositiveIntegerField for Stock**
   - **Why**: Stock cannot be negative
   - **Benefit**: Database-level constraint prevents invalid data
   - **Range**: 0 to 2,147,483,647

5. **Timestamp Tracking**
   - **created_at**: Auto-set on creation (`auto_now_add=True`)
   - **Future**: Add `updated_at` with `auto_now=True`

### Serialization Layer

#### ProductSerializer

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

**Responsibilities:**

1. **Deserialization**: JSON → Python objects
2. **Serialization**: Python objects → JSON
3. **Validation**: Input data validation
4. **Nested representations**: Handle related objects

**Current State:**
- Uses automatic field generation (`fields = "__all__"`)
- No custom validation logic
- All fields are read-write

**Recommended Enhancements:**

```python
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['id', 'created_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
    
    def validate_sku(self, value):
        return value.strip().upper()  # Normalize SKU
```

### API Layer (ViewSets)

#### ProductViewSet

```python
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

**Automatically Provided Methods:**

| Method | Action | HTTP Method | URL Pattern |
|--------|--------|-------------|-------------|
| `list()` | List all products | GET | `/api/products/` |
| `create()` | Create a product | POST | `/api/products/` |
| `retrieve()` | Get single product | GET | `/api/products/{id}/` |
| `update()` | Full update | PUT | `/api/products/{id}/` |
| `partial_update()` | Partial update | PATCH | `/api/products/{id}/` |
| `destroy()` | Delete product | DELETE | `/api/products/{id}/` |

**Request/Response Flow:**

```
1. HTTP Request arrives
        ↓
2. URL Router matches pattern
        ↓
3. ViewSet method called
        ↓
4. Serializer validates data
        ↓
5. Model operation performed
        ↓
6. Serializer formats response
        ↓
7. HTTP Response returned
```

### Routing Layer

#### URL Configuration

**Project-level URLs** (`inventory_project/urls.py`):
```python
urlpatterns = [
    path('admin/', admin.site.urls),      # Admin interface
    path('api/', include('inventory.urls')) # API endpoints
]
```

**App-level URLs** (`inventory/urls.py`):
```python
router = DefaultRouter()
router.register(r'products', ProductViewSet)
urlpatterns = router.urls
```

**Generated Endpoints:**

```
/api/products/           # List and Create
/api/products/{id}/      # Retrieve, Update, Delete
/api/products/{id}/json/ # Schema endpoint
```

## 🔄 Data Flow

### CREATE Product Flow

```
┌─────────┐
│ Client  │
└────┬────┘
     │ POST /api/products/
     │ {name, sku, price, stock}
     ▼
┌─────────────────┐
│  URL Router     │
└────┬────────────┘
     │ Routes to ProductViewSet.create()
     ▼
┌─────────────────┐
│  ViewSet        │ Calls serializer.is_valid()
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│  Serializer     │ Validates data
└────┬────────────┘
     │ Valid? 
     │ Yes ──────► serializer.save()
     │                     │
     │                     ▼
     │              ┌──────────────┐
     │              │    Model     │ Create Product instance
     │              └──────┬───────┘
     │                     │
     │                     ▼
     │              ┌──────────────┐
     │              │   Database   │ INSERT operation
     │              └──────┬───────┘
     │                     │
     │                     ▼
     │              Return saved instance
     │◄─────────────────────┘
     │
     ▼
┌─────────────────┐
│  Serializer     │ Convert to JSON
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│  Response       │ 201 Created + JSON data
└────┬────────────┘
     │
     ▼
┌─────────┐
│ Client  │ Receives response
└─────────┘
```

### READ Product Flow

```
Client
  │
  ├─ GET /api/products/          ──► List all products
  │   └─► Product.objects.all()
  │        └─► SELECT * FROM inventory_product
  │
  └─ GET /api/products/{uuid}/   ──► Get specific product
      └─► Product.objects.get(pk=uuid)
           └─► SELECT * FROM inventory_product WHERE id = {uuid}
```

## 🗄️ Database Schema

### Current Schema

```sql
CREATE TABLE inventory_product (
    id CHAR(32) PRIMARY KEY,              -- UUID stored as char
    name VARCHAR(100) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL CHECK (stock >= 0),
    created_at DATETIME NOT NULL
);

CREATE UNIQUE INDEX idx_product_sku ON inventory_product(sku);
CREATE INDEX idx_product_created ON inventory_product(created_at);
```

### Indexes

| Index | Type | Columns | Purpose |
|-------|------|---------|---------|
| PRIMARY KEY | B-Tree | id | Fast lookups by UUID |
| UNIQUE | B-Tree | sku | Enforce uniqueness, fast SKU lookups |
| *(recommended)* | B-Tree | created_at | Fast sorting by creation date |

## 🔐 Security Architecture

### Current Security Measures

1. **CSRF Protection**: Enabled via Django middleware
2. **SQL Injection**: Protected by Django ORM parameterization
3. **XSS**: Limited exposure (API only, no templates)
4. **Unique Constraints**: Prevents duplicate SKUs

### Security Gaps (To Address)

⚠️ **Missing Security Features:**

1. **Authentication**: No user authentication
2. **Authorization**: No permission checks
3. **Rate Limiting**: No protection against abuse
4. **Input Sanitization**: Minimal validation
5. **Secrets Management**: Hardcoded SECRET_KEY

### Recommended Security Architecture

```
┌─────────────────────────────────────────────────┐
│              Security Layers                     │
├─────────────────────────────────────────────────┤
│  1. Network Layer                               │
│     • HTTPS/TLS                                 │
│     • Rate Limiting (nginx/API Gateway)         │
│     • DDoS Protection                           │
├─────────────────────────────────────────────────┤
│  2. Application Layer                           │
│     • JWT Authentication                        │
│     • Permission Classes                        │
│     • Input Validation                          │
│     • CORS Policy                               │
├─────────────────────────────────────────────────┤
│  3. Business Logic Layer                        │
│     • Authorization Rules                       │
│     • Data Access Controls                      │
│     • Audit Logging                             │
├─────────────────────────────────────────────────┤
│  4. Data Layer                                  │
│     • Database Constraints                      │
│     • Encrypted Connections                     │
│     • Backup & Recovery                         │
└─────────────────────────────────────────────────┘
```

## 📊 Performance Considerations

### Current Performance Characteristics

1. **Query Efficiency**: Simple queries with minimal overhead
2. **Serialization**: Automatic field mapping is fast for simple models
3. **Database**: SQLite suitable for development, limited for production

### Optimization Opportunities

1. **Database Indexing**
   ```python
   class Meta:
       indexes = [
           models.Index(fields=['sku']),
           models.Index(fields=['created_at']),
           models.Index(fields=['stock']),
       ]
   ```

2. **Query Optimization**
   ```python
   # Add select_related/prefetch_related for relationships
   queryset = Product.objects.select_related('category')
   ```

3. **Pagination**
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 50
   }
   ```

4. **Caching**
   ```python
   from django.views.decorators.cache import cache_page
   
   @cache_page(60 * 15)  # Cache for 15 minutes
   def cached_view(request):
       pass
   ```

## 🔄 Scalability Path

### Current State: Monolithic Architecture

```
┌─────────────────────────────────┐
│     Single Django Application   │
│                                 │
│  ┌─────────┐    ┌────────────┐ │
│  │  API    │───►│  Database  │ │
│  └─────────┘    └────────────┘ │
└─────────────────────────────────┘
```

### Scaling Strategy

**Phase 1: Vertical Scaling**
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add caching layer (Redis)

**Phase 2: Horizontal Scaling**
```
         ┌──────────────┐
         │ Load Balancer│
         └───────┬──────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    ┌────┐   ┌────┐   ┌────┐
    │App1│   │App2│   │App3│
    └─┬──┘   └─┬──┘   └─┬──┘
      │        │        │
      └────────┼────────┘
               ▼
        ┌─────────────┐
        │  Database   │
        │  (Primary)  │
        └─────────────┘
```

**Phase 3: Microservices** (Future)
- Product Service
- Inventory Service
- Analytics Service
- Message Queue (RabbitMQ/Kafka)

## 🧩 Design Patterns Used

### 1. Model-View-Controller (MVC)
- **Model**: `Product` model
- **View**: `ProductViewSet`
- **Controller**: URL routing

### 2. Serializer Pattern
- Transforms data between layers
- Validates input/output

### 3. Repository Pattern (via ORM)
- Django ORM abstracts data access
- `Product.objects.all()` etc.

### 4. Dependency Injection
- ViewSet receives serializer class
- Settings injected via Django configuration

## 🔮 Future Architecture Considerations

### Potential Enhancements

1. **Service Layer**
   ```python
   # services/product_service.py
   class ProductService:
       def adjust_stock(self, product_id, amount):
           # Business logic here
           pass
       
       def calculate_total_value(self):
           # Aggregate calculations
           pass
   ```

2. **Event-Driven Architecture**
   - Emit events on product changes
   - Enable audit trails
   - Support real-time updates

3. **API Versioning**
   ```python
   # /api/v1/products/
   # /api/v2/products/
   ```

4. **GraphQL Alternative**
   - More flexible queries
   - Reduce over-fetching
   - Better for complex relationships

## 📈 Monitoring & Observability

### Recommended Instrumentation

1. **Logging**
   - Request/Response logging
   - Error tracking
   - Audit trails

2. **Metrics**
   - Request rate
   - Response time
   - Error rate
   - Database query time

3. **Tracing**
   - Distributed tracing (OpenTelemetry)
   - Request flow tracking
   - Performance bottleneck identification

---

**Document Version:** 1.0.0  
**Last Updated:** January 2026  
**Maintained By:** Development Team

