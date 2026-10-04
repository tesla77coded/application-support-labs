# REST API Troubleshooting

## Overview

REST APIs allow applications and services to communicate over HTTP.

For Application Support and Technical Support roles, API troubleshooting is primarily about determining **where a request is failing and why**.

A support engineer should be able to:

- Understand an API endpoint
- Identify HTTP methods and parameters
- Inspect request headers and body
- Understand authentication and authorization failures
- Interpret HTTP status codes
- Reproduce issues using tools such as `curl`
- Compare expected and actual API behavior
- Use application logs and database information to isolate the failing component
- Escalate incidents with useful technical evidence

---

## 1. REST API Concepts

### Resource

A resource represents an object or entity managed by an application.

Examples:

- Users
- Orders
- Payments
- Products
- Tickets

### Endpoint

An endpoint is a specific API interface used to interact with a resource.

Examples:

```text
GET /api/users
GET /api/users/42
GET /api/orders/5005
POST /api/orders
```

The endpoint defines where and how the client communicates with the application.

---

## 2. HTTP Methods

Common REST API methods:

| Method | Typical Purpose | Example |
|---|---|---|
| GET | Retrieve data | `GET /api/orders/5005` |
| POST | Create a resource | `POST /api/orders` |
| PUT | Replace/update a resource | `PUT /api/users/42` |
| PATCH | Partially update a resource | `PATCH /api/users/42` |
| DELETE | Delete a resource | `DELETE /api/users/42` |

When troubleshooting an API issue, verify that the client is using the **correct HTTP method for the endpoint**.

---

## 3. Path Parameters and Query Parameters

### Path Parameters

Path parameters identify a specific resource.

```text
GET /api/orders/5005
```

Here:

```text
5005
```

is the order ID.

Another example:

```text
GET /api/users/42
```

The path parameter is:

```text
42
```

### Query Parameters

Query parameters modify or filter a request.

```text
GET /api/orders?status=pending
```

Multiple parameters can be used:

```text
GET /api/orders?status=pending&limit=20
```

Here:

```text
status=pending
limit=20
```

are query parameters.

### Troubleshooting

When an API request fails, verify:

1. The endpoint path is correct.
2. The resource ID is correct.
3. Query parameter names are correct.
4. Parameter values have the expected format.
5. Required parameters have been provided.

---

## 4. Authentication vs Authorization

These are two different stages of access control.

### Authentication

Authentication answers:

> Who are you?

Example:

```http
Authorization: Bearer <token>
```

A missing, invalid, or expired token can result in:

```text
401 Unauthorized
```

### Authorization

Authorization answers:

> Are you allowed to perform this action?

A user can be successfully authenticated but lack permission to access a resource.

This commonly results in:

```text
403 Forbidden
```

### Support Investigation

For a `401`:

- Check whether authentication credentials were supplied.
- Verify the `Authorization` header.
- Check whether the token is expired or invalid.
- Check authentication-related logs.

For a `403`:

- Confirm the user is authenticated.
- Check the user's role or permissions.
- Verify whether the resource/action requires additional privileges.

---

## 5. Request and Response Validation

An API request can fail even when the HTTP request itself is technically valid.

Example:

```http
POST /api/orders
Content-Type: application/json
```

```json
{
  "product_id": 1001,
  "quantity": 0
}
```

The JSON is syntactically valid.

However, the API may require:

```text
quantity > 0
```

The request can therefore be rejected with:

```text
400 Bad Request
```

### What to Check

When investigating a `400`:

- Is the JSON valid?
- Are all required fields present?
- Are field names correct?
- Are data types correct?
- Are parameter values valid?
- Does the request match the API contract?
- Are there validation rules being violated?

---

## 6. API Contract

The API contract defines how an API is expected to behave.

It may specify:

- Endpoint
- HTTP method
- Required headers
- Authentication requirements
- Request parameters
- Request body structure
- Data types
- Required fields
- Response structure
- Possible error responses

Example:

```text
POST /api/users
```

Expected body:

```json
{
  "name": "Rahul",
  "email": "rahul@example.com",
  "password": "example123"
}
```

If `password` is required but omitted, the request may fail validation.

A support engineer should use the API documentation or contract before assuming that a request is incorrect.

---

## 7. A Practical API Troubleshooting Workflow

When an API issue is reported, investigate systematically.

### Step 1 — Reproduce the Issue

Try to reproduce the customer's request.

Example:

```bash
curl -i https://api.shop.example.com/api/orders/5005
```

Record:

- HTTP method
- Endpoint
- Parameters
- Headers
- Request body
- Status code
- Response body

---

### Step 2 — Check Authentication

If the response is:

```text
401 Unauthorized
```

investigate authentication first.

Example:

```bash
curl -i \
  -H "Authorization: Bearer <token>" \
  https://api.shop.example.com/api/orders/5005
```

Do not spend time investigating database performance if authentication has not succeeded yet.

---

### Step 3 — Check Authorization

If authentication succeeds but the response is:

```text
403 Forbidden
```

investigate:

- User role
- Permissions
- Resource ownership
- Access policies

---

### Step 4 — Validate the Endpoint and Parameters

Check:

```text
/api/orders/5005
```

Verify:

- Endpoint exists
- HTTP method is correct
- Order ID is valid
- Query parameters are correct
- Required parameters are present

---

### Step 5 — Inspect the Status Code

Use the status code to determine the next investigation area.

Examples:

```text
400 → request/validation
401 → authentication
403 → authorization
404 → endpoint/resource
409 → state/conflict
429 → rate limiting
500 → application/server
502 → upstream service
503 → service availability
504 → upstream timeout
```

The status code narrows the investigation but does not necessarily identify the root cause.

---

### Step 6 — Inspect the Response Body

The response body may contain useful diagnostic information.

Example:

```json
{
  "error": "Order service unavailable"
}
```

or:

```json
{
  "error": "Invalid order ID"
}
```

Do not rely only on the HTTP status code.

---

### Step 7 — Check Application Logs

Search application logs using:

- Timestamp
- Endpoint
- User ID
- Request ID
- Order ID
- Error message

Example:

```text
2026-10-03 14:32:11 INFO GET /api/orders/5005 request_id=REQ-9821
2026-10-03 14:32:11 INFO Authentication successful user_id=721
2026-10-03 14:32:11 INFO Database query started request_id=REQ-9821
2026-10-03 14:32:56 ERROR Database query timeout request_id=REQ-9821
```

The `request_id` is particularly useful because it allows the request to be traced through multiple application components.

---

### Step 8 — Check Dependencies

If the application depends on another service or database, investigate that dependency.

Examples:

```text
Application
    ↓
Order Service
    ↓
Database
```

or:

```text
Client
    ↓
API Gateway
    ↓
Order Service
    ↓
Payment Service
    ↓
Database
```

A problem in a downstream dependency can cause the API request to fail even when the API service itself is running.

---

## 8. Example: Troubleshooting a 504

Customer reports:

> "I cannot view order 5005."

Initial request:

```bash
curl -i https://api.shop.example.com/api/orders/5005
```

Response:

```text
HTTP/2 401 Unauthorized
```

Investigation:

```text
Authentication credentials were missing.
```

Retry with a valid bearer token:

```bash
curl -i \
  -H "Authorization: Bearer <token>" \
  https://api.shop.example.com/api/orders/5005
```

Response:

```text
HTTP/2 504 Gateway Timeout
```

Application logs show:

```text
Authentication successful
Database query started
Database query timeout
Failed to fetch order
Upstream dependency timeout
```

Further investigation shows:

```text
Database CPU: 94%
Active connections: 198/200
Long-running queries: 17
Normal query time: <100 ms
Current query time: 40–50 seconds
```

A TCP connectivity test succeeds:

```bash
nc -vz db-prod-01 5432
```

### Assessment

There is no evidence of a basic database network connectivity failure.

The evidence strongly indicates a **database performance/resource contention issue**.

However, the exact root cause has not yet been established.

Possible areas for DBA/developer investigation include:

- Long-running queries
- Query execution plans
- Missing or ineffective indexes
- Lock contention
- High database CPU
- Connection saturation
- Recent database/application changes

### Support Escalation

A useful escalation would contain:

```text
Incident:
Customer unable to retrieve order 5005.

Impact:
Order retrieval fails with HTTP 504 after successful authentication.

Evidence:
- Authentication succeeds.
- API returns 504.
- Database query takes 40–50 seconds instead of <100 ms.
- Database CPU is 94%.
- 198/200 database connections are active.
- 17 long-running queries are present.
- TCP connectivity to database port 5432 succeeds.

Assessment:
Evidence points toward database performance/resource contention.
Basic network connectivity failure has not been observed.

Recommended investigation:
DBA/development team to investigate long-running queries,
CPU saturation, connection usage, locks, indexes, and query
execution plans.
```

This is a much stronger escalation than simply saying:

```text
"API is down. Please check."
```

---

## 9. Common API Troubleshooting Mistakes

### Mistake 1 — Assuming 200 Means Everything Worked

```text
HTTP 200
```

means the HTTP request was successfully handled.

It does not automatically mean the expected business operation succeeded.

Always inspect the response body and application behavior.

---

### Mistake 2 — Treating Every 500 as a Network Problem

A `500` indicates an internal server-side error.

Possible causes include:

- Application exception
- Database failure
- Dependency failure
- Configuration problem
- Unexpected application state

Check logs and dependencies before deciding on the root cause.

---

### Mistake 3 — Treating Every 4xx as "User Error"

A `4xx` response indicates that the request cannot be fulfilled as made, but the reason still needs investigation.

For example:

```text
401 → authentication
403 → authorization
404 → endpoint/resource
409 → state conflict
429 → rate limiting
```

---

### Mistake 4 — Changing Production Data Immediately

If an API fails because of a database issue, do not immediately modify or delete production data.

First:

1. Collect evidence.
2. Identify the failing component.
3. Check logs and monitoring.
4. Follow the organization's runbook/change process.
5. Escalate when required.

---

## 10. Support Engineer Mental Model

A useful way to think about API troubleshooting is:

```text
Request
   ↓
Authentication
   ↓
Authorization
   ↓
