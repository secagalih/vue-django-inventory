# API Documentation

Complete API reference for the Inventory Management System backend.

## 📍 Base URL

```
Development: http://localhost:8000/api/
Production: https://your-domain.com/api/
```

## 🔐 Authentication

**Current Status:** No authentication required (⚠️ Development only)

**Recommended for Production:**
- JWT Token Authentication
- Session Authentication
- OAuth2

### Future Authentication Header

```http
Authorization: Bearer <your-jwt-token>
```

## 📋 API Endpoints Overview

| Endpoint | Method | Description | Status Code |
|----------|--------|-------------|-------------|
| `/api/products/` | GET | List all products | 200 |
| `/api/products/` | POST | Create a new product | 201 |
| `/api/products/{id}/` | GET | Retrieve a specific product | 200 |
| `/api/products/{id}/` | PUT | Full update of a product | 200 |
| `/api/products/{id}/` | PATCH | Partial update of a product | 200 |
| `/api/products/{id}/` | DELETE | Delete a product | 204 |

---

## 📦 Product Endpoints

### 1. List All Products

Retrieve a list of all products in the inventory.

**Endpoint:** `GET /api/products/`

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| None (currently) | - | No filtering implemented yet | - |

**Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "Wireless Mouse",
    "sku": "WM-001",
    "price": "29.99",
    "stock": 150,
    "created_at": "2026-01-06T10:30:00Z"
  },
  {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "name": "USB Keyboard",
    "sku": "KB-002",
    "price": "49.99",
    "stock": 75,
    "created_at": "2026-01-06T11:15:00Z"
  }
]
```

**Example Request:**

```bash
curl -X GET http://localhost:8000/api/products/
```

```javascript
// JavaScript (fetch)
fetch('http://localhost:8000/api/products/')
  .then(response => response.json())
  .then(data => console.log(data));
```

```python
# Python (requests)
import requests
response = requests.get('http://localhost:8000/api/products/')
products = response.json()
```

---

### 2. Create a Product

Create a new product in the inventory.

**Endpoint:** `POST /api/products/`

**Request Headers:**

```http
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "price": "29.99",
  "stock": 150
}
```

**Field Specifications:**

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | Yes | Max 100 chars | Product name |
| `sku` | string | Yes | Max 50 chars, unique | Stock Keeping Unit |
| `price` | decimal | Yes | Max 10 digits, 2 decimal places | Product price |
| `stock` | integer | No | Non-negative, default: 0 | Current stock quantity |

**Success Response:**

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "price": "29.99",
  "stock": 150,
  "created_at": "2026-01-06T12:00:00Z"
}
```

**Error Responses:**

**400 Bad Request** - Validation error

```json
{
  "sku": [
    "product with this sku already exists."
  ]
}
```

```json
{
  "price": [
    "Ensure that there are no more than 10 digits in total."
  ]
}
```

```json
{
  "name": [
    "This field is required."
  ]
}
```

**Example Requests:**

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

```javascript
// JavaScript (fetch)
fetch('http://localhost:8000/api/products/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'Wireless Mouse',
    sku: 'WM-001',
    price: '29.99',
    stock: 150
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

```python
# Python (requests)
import requests

data = {
    "name": "Wireless Mouse",
    "sku": "WM-001",
    "price": "29.99",
    "stock": 150
}

response = requests.post(
    'http://localhost:8000/api/products/',
    json=data
)
product = response.json()
```

---

### 3. Retrieve a Specific Product

Get details of a single product by its UUID.

**Endpoint:** `GET /api/products/{id}/`

**URL Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | The unique identifier of the product |

**Success Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "price": "29.99",
  "stock": 150,
  "created_at": "2026-01-06T12:00:00Z"
}
```

**Error Response:**

**404 Not Found** - Product doesn't exist

```json
{
  "detail": "Not found."
}
```

**Example Requests:**

```bash
curl -X GET http://localhost:8000/api/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890/
```

```javascript
// JavaScript (fetch)
const productId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
fetch(`http://localhost:8000/api/products/${productId}/`)
  .then(response => response.json())
  .then(data => console.log(data));
```

```python
# Python (requests)
import requests

product_id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
response = requests.get(f'http://localhost:8000/api/products/{product_id}/')
product = response.json()
```

---

### 4. Full Update (Replace) a Product

Replace all fields of an existing product.

**Endpoint:** `PUT /api/products/{id}/`

**Request Headers:**

```http
Content-Type: application/json
```

**Request Body:**

```json
{
  "name": "Wireless Mouse Pro",
  "sku": "WM-001",
  "price": "39.99",
  "stock": 200
}
```

**Note:** All fields must be provided. Missing fields will result in validation errors.

**Success Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Wireless Mouse Pro",
  "sku": "WM-001",
  "price": "39.99",
  "stock": 200,
  "created_at": "2026-01-06T12:00:00Z"
}
```

**Error Responses:**

**400 Bad Request** - Validation error  
**404 Not Found** - Product doesn't exist

**Example Request:**

```bash
curl -X PUT http://localhost:8000/api/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse Pro",
    "sku": "WM-001",
    "price": "39.99",
    "stock": 200
  }'
```

---

### 5. Partial Update a Product

Update only specific fields of a product.

**Endpoint:** `PATCH /api/products/{id}/`

**Request Headers:**

```http
Content-Type: application/json
```

**Request Body:**

```json
{
  "stock": 175
}
```

**Note:** Only include fields you want to update. Other fields remain unchanged.

**Success Response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "price": "29.99",
  "stock": 175,
  "created_at": "2026-01-06T12:00:00Z"
}
```

**Example Requests:**

```bash
# Update only stock
curl -X PATCH http://localhost:8000/api/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Content-Type: application/json" \
  -d '{"stock": 175}'
```

```bash
# Update multiple fields
curl -X PATCH http://localhost:8000/api/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Content-Type: application/json" \
  -d '{
    "price": "27.99",
    "stock": 200
  }'
```

```javascript
// JavaScript (fetch)
const productId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
fetch(`http://localhost:8000/api/products/${productId}/`, {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    stock: 175
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

```python
# Python (requests)
import requests

product_id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
data = {"stock": 175}

response = requests.patch(
    f'http://localhost:8000/api/products/{product_id}/',
    json=data
)
product = response.json()
```

---

### 6. Delete a Product

Remove a product from the inventory.

**Endpoint:** `DELETE /api/products/{id}/`

**Success Response:**

```http
HTTP/1.1 204 No Content
```

No response body is returned on successful deletion.

**Error Response:**

**404 Not Found** - Product doesn't exist

```json
{
  "detail": "Not found."
}
```

**Example Requests:**

```bash
curl -X DELETE http://localhost:8000/api/products/a1b2c3d4-e5f6-7890-abcd-ef1234567890/
```

```javascript
// JavaScript (fetch)
const productId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
fetch(`http://localhost:8000/api/products/${productId}/`, {
  method: 'DELETE'
})
.then(response => {
  if (response.status === 204) {
    console.log('Product deleted successfully');
  }
});
```

```python
# Python (requests)
import requests

product_id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
response = requests.delete(f'http://localhost:8000/api/products/{product_id}/')

if response.status_code == 204:
    print('Product deleted successfully')
```

---

## 🔍 Data Models

### Product Model

```json
{
  "id": "uuid",
  "name": "string",
  "sku": "string",
  "price": "decimal",
  "stock": "integer",
  "created_at": "datetime"
}
```

#### Field Details

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | UUID | Unique identifier | Auto-generated, read-only |
| `name` | String | Product name | Max 100 characters, required |
| `sku` | String | Stock Keeping Unit | Max 50 characters, unique, required |
| `price` | Decimal | Product price | Max 10 digits total, 2 decimal places, required |
| `stock` | Integer | Quantity in stock | Non-negative, default: 0 |
| `created_at` | DateTime | Creation timestamp | Auto-generated, read-only |

---

## ⚠️ Error Handling

### Standard Error Response Format

```json
{
  "field_name": [
    "Error message describing the issue."
  ]
}
```

### Common HTTP Status Codes

| Status Code | Meaning | When Used |
|-------------|---------|-----------|
| 200 OK | Success | GET, PUT, PATCH successful |
| 201 Created | Resource created | POST successful |
| 204 No Content | Success with no body | DELETE successful |
| 400 Bad Request | Validation error | Invalid input data |
| 404 Not Found | Resource not found | Invalid ID in URL |
| 500 Internal Server Error | Server error | Unexpected server issue |

### Example Error Responses

**Duplicate SKU:**
```json
{
  "sku": [
    "product with this sku already exists."
  ]
}
```

**Missing Required Field:**
```json
{
  "name": [
    "This field is required."
  ]
}
```

**Invalid Data Type:**
```json
{
  "price": [
    "A valid number is required."
  ]
}
```

**Negative Stock (if validation added):**
```json
{
  "stock": [
    "Ensure this value is greater than or equal to 0."
  ]
}
```

---

## 📊 Response Examples

### Empty List

```json
[]
```

### Single Product

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Wireless Mouse",
  "sku": "WM-001",
  "price": "29.99",
  "stock": 150,
  "created_at": "2026-01-06T12:00:00Z"
}
```

### Product List

```json
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "Wireless Mouse",
    "sku": "WM-001",
    "price": "29.99",
    "stock": 150,
    "created_at": "2026-01-06T10:30:00Z"
  },
  {
    "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
    "name": "USB Keyboard",
    "sku": "KB-002",
    "price": "49.99",
    "stock": 75,
    "created_at": "2026-01-06T11:15:00Z"
  }
]
```

---

## 🔮 Future Enhancements

### Planned Features (Not Yet Implemented)

#### 1. Filtering
```
GET /api/products/?stock__gte=10
GET /api/products/?sku=WM-001
GET /api/products/?price__lt=50
```

#### 2. Ordering
```
GET /api/products/?ordering=price
GET /api/products/?ordering=-created_at
```

#### 3. Search
```
GET /api/products/?search=mouse
```

#### 4. Pagination
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

#### 5. Custom Actions
```
POST /api/products/{id}/adjust_stock/
POST /api/products/{id}/low_stock_alert/
```

---

## 🧪 Testing the API

### Using cURL

```bash
# List products
curl http://localhost:8000/api/products/

# Create product
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","sku":"TEST-001","price":"9.99","stock":5}'

# Get specific product
curl http://localhost:8000/api/products/{id}/

# Update product
curl -X PATCH http://localhost:8000/api/products/{id}/ \
  -H "Content-Type: application/json" \
  -d '{"stock":10}'

# Delete product
curl -X DELETE http://localhost:8000/api/products/{id}/
```

### Using Postman

1. Import the base URL: `http://localhost:8000/api/`
2. Create requests for each endpoint
3. Set `Content-Type: application/json` header
4. Add request body for POST/PUT/PATCH requests

### Using Python

```python
import requests

BASE_URL = 'http://localhost:8000/api'

# List products
response = requests.get(f'{BASE_URL}/products/')
print(response.json())

# Create product
product_data = {
    'name': 'Test Product',
    'sku': 'TEST-001',
    'price': '19.99',
    'stock': 10
}
response = requests.post(f'{BASE_URL}/products/', json=product_data)
print(response.status_code, response.json())
```

---

## 📝 Notes

1. **UUID Format**: All IDs are in UUID format (e.g., `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)
2. **DateTime Format**: All timestamps use ISO 8601 format with UTC timezone
3. **Decimal Precision**: Prices maintain exactly 2 decimal places
4. **CORS**: CORS is enabled for cross-origin requests during development

---

**API Version:** 1.0  
**Last Updated:** January 2026  
**Base URL:** `http://localhost:8000/api/`

