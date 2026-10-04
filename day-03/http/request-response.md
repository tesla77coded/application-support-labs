
# HTTP Request and Response

## Overview

HTTP is the communication protocol used between clients and web servers and is fundamental to application and API troubleshooting.

An HTTP transaction consists of:

1. A client sending an HTTP request.
2. A server processing the request.
3. The server returning an HTTP response.

Understanding the structure of both is essential when investigating API and application issues.

---

## HTTP Request

An HTTP request contains several components:

- Request method
- Request path
- HTTP version
- Request headers
- Optional request body

### Example

```http
POST /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json

{
    "name": "Rahul",
    "email": "rahul@example.com"
}
```

### Request Line

```http
POST /api/users HTTP/1.1
```

The request line contains:

| Component    | Purpose                          |
| ------------ | -------------------------------- |
| `POST`       | HTTP method used for the request |
| `/api/users` | Request path/resource            |
| `HTTP/1.1`   | HTTP protocol version            |

---

## Request Headers

Headers provide additional information about the request.

### Host

```http
Host: api.example.com
```

Identifies the host/server being requested.

### Authorization

```http
Authorization: Bearer <token>
```

Carries authentication credentials such as a bearer token.

A missing, invalid, or expired credential can result in an authentication failure such as:

```http
401 Unauthorized
```

### Content-Type

```http
Content-Type: application/json
```

Specifies the format of the request body.

In this example, the request body contains JSON.

### Accept

```http
Accept: application/json
```

Indicates the response format preferred by the client.

A useful distinction:

```text
Content-Type
→ What format am I sending?

Accept
→ What response format do I prefer?
```

---

## Request Body

The request body contains data submitted to the server when required.

Example:

```json
{
    "name": "Rahul",
    "email": "rahul@example.com"
}
```

Not every HTTP request requires a body. For example, a simple `GET` request commonly retrieves information without sending a request body.

---

# HTTP Response

An HTTP response contains:

- Status line
- Response headers
- Optional response body

### Example

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "order_id": 5005,
    "status": "pending"
}
```

### Status Line

```http
HTTP/1.1 200 OK
```

Contains:

| Component  | Purpose               |
| ---------- | --------------------- |
| `HTTP/1.1` | HTTP protocol version |
| `200`      | HTTP status code      |
| `OK`       | Reason phrase         |

The status code is one of the first pieces of evidence to examine during API troubleshooting.

---

## Response Headers

Response headers provide metadata about the response.

Example:

```http
Content-Type: application/json
```

This indicates that the response body contains JSON.

Other response headers may provide information about caching, cookies, content length, redirects, and other aspects of the response.

---

## Response Body

The response body contains the data returned by the server.

Example:

```json
{
    "order_id": 5005,
    "status": "pending"
}
```

Error responses may also contain useful diagnostic information:

```json
{
    "error": "Authentication required"
}
```

The response body should therefore be inspected along with the status code rather than relying on the status code alone.

---

# HTTP Troubleshooting Perspective

When investigating an API issue, inspect the request and response systematically.

### Request-side checks

```text
Method
  ↓
Path / endpoint
  ↓
Parameters
  ↓
Headers
  ↓
Authentication
  ↓
Request body
  ↓
API contract / validation rules
```

### Response-side checks

```text
Status code
  ↓
Response headers
  ↓
Response body
  ↓
Application error information
```

The objective is to determine which layer is responsible for the failure rather than assuming that the API or server is simply "down."

---

# Example: 400 Bad Request

Request:

```http
POST /api/users HTTP/1.1
Content-Type: application/json

{
    "name": "Rahul",
    "email": "rahul@example.com"
}
```

Response:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "error": "password is required"
}
```

Possible investigation:

1. Verify that the endpoint is correct.
2. Verify that the request contains valid JSON.
3. Compare the request body against the API contract.
4. Check required fields.
5. Check field names and data types.
6. Check application-specific validation rules.

A `400` does not automatically indicate that the server itself is broken. The server may be functioning correctly while rejecting an invalid request.

---

# Example: 401 Unauthorized

Request:

```http
GET /api/orders/5005 HTTP/1.1
Accept: application/json
```

Response:

```http
HTTP/1.1 401 Unauthorized

{
    "error": "Authentication required"
}
```

Investigation should focus on authentication:

- Is authentication required?
- Was an authorization credential provided?
- Is the token/API key valid?
- Has the credential expired?
- Is the authorization header correctly formatted?

---

# Example: 403 Forbidden

Request:

```http
GET /api/admin/users HTTP/1.1
Authorization: Bearer <valid-token>
```

Response:

```http
HTTP/1.1 403 Forbidden

{
    "error": "Insufficient permissions"
}
```

The distinction from `401` is important:

```text
401
→ Authentication problem

403
→ Authentication succeeded, but the authenticated identity
  does not have sufficient permission
```

---

# Key Support Takeaways

- An HTTP request contains the information required by the server to process an operation.
- An HTTP response contains the server's result and diagnostic information.
- Headers provide metadata about the request or response.
- `Content-Type` describes the format of the request body.
- `Accept` indicates the response format preferred by the client.
- A request body must satisfy both JSON syntax and the API's expected contract.
- Status codes provide an important starting point for troubleshooting but should be interpreted together with headers, response bodies, logs, and application behavior.
- Successful HTTP communication does not always guarantee a successful business operation.
- Support investigations should use evidence to identify the failing layer before escalating.
# HTTP Request and Response

## Overview

HTTP is the communication protocol used between clients and web servers and is fundamental to application and API troubleshooting.

An HTTP transaction consists of:

1. A client sending an HTTP request.
2. A server processing the request.
3. The server returning an HTTP response.

Understanding the structure of both is essential when investigating API and application issues.

---

## HTTP Request

An HTTP request contains several components:

- Request method
- Request path
- HTTP version
- Request headers
- Optional request body

### Example

```http
POST /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json

{
    "name": "Rahul",
    "email": "rahul@example.com"
}
```

### Request Line

```http
POST /api/users HTTP/1.1
```

The request line contains:

| Component    | Purpose                          |
| ------------ | -------------------------------- |
| `POST`       | HTTP method used for the request |
| `/api/users` | Request path/resource            |
| `HTTP/1.1`   | HTTP protocol version            |

---

## Request Headers

Headers provide additional information about the request.

### Host

```http
Host: api.example.com
```

Identifies the host/server being requested.

### Authorization

```http
Authorization: Bearer <token>
```

Carries authentication credentials such as a bearer token.

A missing, invalid, or expired credential can result in an authentication failure such as:

```http
401 Unauthorized
```

### Content-Type

```http
Content-Type: application/json
```

Specifies the format of the request body.

In this example, the request body contains JSON.

### Accept

```http
Accept: application/json
```

Indicates the response format preferred by the client.

A useful distinction:

```text
Content-Type
→ What format am I sending?

Accept
→ What response format do I prefer?
```

---

## Request Body

The request body contains data submitted to the server when required.

Example:

```json
{
    "name": "Rahul",
    "email": "rahul@example.com"
}
```

Not every HTTP request requires a body. For example, a simple `GET` request commonly retrieves information without sending a request body.

---

# HTTP Response

An HTTP response contains:

- Status line
- Response headers
- Optional response body

### Example

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "order_id": 5005,
    "status": "pending"
}
```

### Status Line

```http
HTTP/1.1 200 OK
```

Contains:

| Component  | Purpose               |
| ---------- | --------------------- |
| `HTTP/1.1` | HTTP protocol version |
| `200`      | HTTP status code      |
| `OK`       | Reason phrase         |

The status code is one of the first pieces of evidence to examine during API troubleshooting.

---

## Response Headers

Response headers provide metadata about the response.

Example:

```http
Content-Type: application/json
```

This indicates that the response body contains JSON.

Other response headers may provide information about caching, cookies, content length, redirects, and other aspects of the response.

---

## Response Body

The response body contains the data returned by the server.

Example:

```json
{
    "order_id": 5005,
    "status": "pending"
}
```

Error responses may also contain useful diagnostic information:

```json
{
    "error": "Authentication required"
}
```

The response body should therefore be inspected along with the status code rather than relying on the status code alone.

---

# HTTP Troubleshooting Perspective

When investigating an API issue, inspect the request and response systematically.

### Request-side checks

```text
Method
  ↓
Path / endpoint
  ↓
Parameters
  ↓
Headers
  ↓
Authentication
  ↓
Request body
  ↓
API contract / validation rules
```

### Response-side checks

```text
Status code
  ↓
Response headers
  ↓
Response body
  ↓
Application error information
```

The objective is to determine which layer is responsible for the failure rather than assuming that the API or server is simply "down."

---

# Example: 400 Bad Request

Request:

```http
POST /api/users HTTP/1.1
Content-Type: application/json

{
    "name": "Rahul",
    "email": "rahul@example.com"
}
```

Response:

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "error": "password is required"
}
```

Possible investigation:

1. Verify that the endpoint is correct.
2. Verify that the request contains valid JSON.
3. Compare the request body against the API contract.
4. Check required fields.
5. Check field names and data types.
6. Check application-specific validation rules.

A `400` does not automatically indicate that the server itself is broken. The server may be functioning correctly while rejecting an invalid request.

---

# Example: 401 Unauthorized

Request:

```http
GET /api/orders/5005 HTTP/1.1
Accept: application/json
```

Response:

```http
HTTP/1.1 401 Unauthorized

{
    "error": "Authentication required"
}
```

Investigation should focus on authentication:

- Is authentication required?
- Was an authorization credential provided?
- Is the token/API key valid?
- Has the credential expired?
- Is the authorization header correctly formatted?

---

# Example: 403 Forbidden

Request:

```http
GET /api/admin/users HTTP/1.1
Authorization: Bearer <valid-token>
```

Response:

```http
HTTP/1.1 403 Forbidden

{
    "error": "Insufficient permissions"
}
```

The distinction from `401` is important:

```text
401
→ Authentication problem

403
→ Authentication succeeded, but the authenticated identity
  does not have sufficient permission
```

---

# Key Support Takeaways

- An HTTP request contains the information required by the server to process an operation.
- An HTTP response contains the server's result and diagnostic information.
- Headers provide metadata about the request or response.
- `Content-Type` describes the format of the request body.
- `Accept` indicates the response format preferred by the client.
- A request body must satisfy both JSON syntax and the API's expected contract.
- Status codes provide an important starting point for troubleshooting but should be interpreted together with headers, response bodies, logs, and application behavior.
- Successful HTTP communication does not always guarantee a successful business operation.
- Support investigations should use evidence to identify the failing layer before escalating.
