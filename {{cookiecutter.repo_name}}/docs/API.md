# API Documentation

REST API documentation for {{ cookiecutter.project_name }}.

## Base URL

- **Development**: `http://localhost:8000/api/`
- **Staging**: `https://api-staging.example.com/api/`
- **Production**: `https://api.example.com/api/`

## Authentication

{% if cookiecutter.use_drf == 'y' %}
### Session Authentication
Used for browser-based requests and admin panel.

```bash
POST /api/auth/login/
{
  "username": "user@example.com",
  "password": "password"
}
```

### Token Authentication (Optional)
Enable in settings if needed:

```bash
Authorization: Token your-token-here
```
{% endif %}

## API Schema

Access the OpenAPI schema at:

- **Swagger UI**: `/api/schema/swagger/`
- **ReDoc**: `/api/schema/redoc/`
- **OpenAPI JSON**: `/api/schema/`

## Response Format

### Successful Response
```json
{
  "data": { ... },
  "success": true,
  "error": null
}
```

### Error Response
```json
{
  "data": null,
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": [ ... ]
  }
}
```

## Pagination

List endpoints support pagination:

```bash
GET /api/resource/?page=1&page_size=20
```

Response includes:
- `count`: Total number of results
- `next`: URL to next page
- `previous`: URL to previous page
- `results`: Array of results

## Filtering & Search

### Filter
```bash
GET /api/resource/?status=active&created_after=2024-01-01
```

### Search
```bash
GET /api/resource/?search=keyword
```

### Ordering
```bash
GET /api/resource/?ordering=-created_at
```

## Common Endpoints

### Health Check
```bash
GET /health/
200 OK
{"status": "ok"}
```

### List Resources
```bash
GET /api/resource/
200 OK
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [ ... ]
}
```

### Create Resource
```bash
POST /api/resource/
Content-Type: application/json

{
  "field1": "value1",
  "field2": "value2"
}

201 Created
{ ... }
```

### Retrieve Resource
```bash
GET /api/resource/{id}/
200 OK
{ ... }
```

### Update Resource
```bash
PUT /api/resource/{id}/
PATCH /api/resource/{id}/
200 OK
{ ... }
```

### Delete Resource
```bash
DELETE /api/resource/{id}/
204 No Content
```

## Error Codes

Common error codes returned:

| Code | Status | Meaning |
|------|--------|---------|
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | No permission |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict |
| `VALIDATION_ERROR` | 400 | Validation failed |
| `INTERNAL_ERROR` | 500 | Server error |

## Rate Limiting

API requests are rate-limited per endpoint. Check headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1234567890
```

## Versioning

API is currently at `v1`. Future versions will use:
- `/api/v2/resource/`

## Changelog

See `CHANGELOG.md` for API changes and breaking changes.

---

**Last Updated**: 2026-07-29
