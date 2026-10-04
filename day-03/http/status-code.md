# HTTP Status Codes — Application Support

## Overview

HTTP status codes communicate the result of an HTTP request.

For Application Support, the status code is an important troubleshooting signal, but it should not be interpreted in isolation. The request, response body, application logs, dependencies, and business behavior may provide additional context.

---

## Status Code Categories

| Range | Category | Support Perspective |
|---|---|---|
| `2xx` | Success | Request was successfully handled |
| `3xx` | Redirection | Client or resource has been redirected |
| `4xx` | Client/request condition | Request cannot be fulfilled as submitted |
| `5xx` | Server-side condition | Failure occurred while processing the request or communicating with a dependency |

---

# 2xx — Successful Requests

## 200 OK

The request was successfully handled.

Example:

```http
GET /api/orders/5005

HTTP/1.1 200 OK
```

### Support investigation

A `200` indicates successful HTTP handling, but the response should still be checked to determine whether the expected business result was returned.

```text
200 OK
   ↓
Inspect response body
   ↓
Confirm expected result
```

---

## 201 Created

Indicates that a new resource was successfully created.

Example:

```http
POST /api/users

HTTP/1.1 201 Created
```

Commonly associated with resource-creation operations.

---

## 204 No Content

Indicates that the request was successfully processed but there is no response body.

Example:

```http
DELETE /api/users/501

HTTP/1.1 204 No Content
```

A missing response body is expected for this status.

---

# 4xx — Request / Client-Side Conditions

## 400 Bad Request

The server cannot process the request because the request is invalid.

Common causes:

- Malformed JSON
- Missing required fields
- Invalid field values
- Incorrect data types
- Invalid parameters
- API contract validation failures

### Investigation

```text
400
 ↓
Check response body
 ↓
Check request syntax
 ↓
Check headers
 ↓
Check parameters
 ↓
Compare payload with API contract
 ↓
Check validation rules
```

A `400` does not necessarily indicate a server failure.

---

## 401 Unauthorized

Authentication is required or the supplied authentication credentials cannot be accepted.

Common causes:

- Missing authentication token
- Invalid token
- Expired token
- Invalid API key
- Incorrect authorization-header format

### Investigation

```text
401
 ↓
Is authentication required?
 ↓
Was a credential supplied?
 ↓
Is it valid?
 ↓
Has it expired?
 ↓
Is the header correctly formatted?
```

### Key distinction

```text
401
→ Authentication problem
```

---

## 403 Forbidden

The request was understood and the identity was authenticated, but the identity does not have sufficient permission.

Common causes:

- Insufficient role
- Missing permission
- Insufficient OAuth scope
- Resource-access restriction

### Investigation

```text
403
 ↓
Who is authenticated?
 ↓
What role/permissions/scopes do they have?
 ↓
What does the endpoint require?
```

### Key distinction

```text
401
→ "I cannot authenticate you."

403
→ "I know who you are, but you are not permitted to perform this operation."
```

---

## 404 Not Found

The requested resource or endpoint could not be found.

Possible causes:

- Incorrect endpoint/path
- Incorrect resource ID
- Resource does not exist
- Incorrect API version or route

Example:

```http
GET /api/orders/5005

HTTP/1.1 404 Not Found
```

### Investigation

```text
404
 ↓
Verify endpoint/path
 ↓
Check API documentation
 ↓
Verify resource identifier
 ↓
Check whether the resource exists
```

Do not immediately assume that the entire API is unavailable.

---

## 409 Conflict

The request conflicts with the current state of the resource.

Example:

```http
POST /api/users

{
    "email": "rahul@example.com"
}

HTTP/1.1 409 Conflict
```

Possible cause:

```text
The email address already exists.
```

Other examples include conflicting updates or attempts to perform an operation that is incompatible with the resource's current state.

### Investigation

Check:

- Current resource state
- Existing records
- Concurrent updates
- Application-specific conflict rules

---

## 429 Too Many Requests

The client has exceeded a configured request rate or API limit.

Possible causes:

- Excessive API requests
- Automated job making too many requests
- Retry loop
- Rate-limit configuration
- Per-user or per-client quota exceeded

A response may include:

```http
Retry-After: 30
```

### Investigation

Check:

- Request volume
- Rate-limit configuration
- Client/application behavior
- Retry mechanisms
- Whether other clients are affected

A `429` does not indicate that the API itself is necessarily unavailable.

---

# 5xx — Server and Dependency Conditions

## 500 Internal Server Error

The server encountered an unexpected condition while processing the request.

Possible causes:

- Unhandled application exception
- Database failure
- Configuration issue
- Unexpected application data
- Dependency failure

### Investigation

```text
500
 ↓
Check application logs
 ↓
Find exception / stack trace
 ↓
Identify failing component
 ↓
Check dependencies
 ↓
Check recent deployments/configuration changes
```

The status code alone does not identify the root cause.

---

## 502 Bad Gateway

A gateway or proxy received an invalid or unusable response from an upstream service.

Typical architecture:

```text
Client
  ↓
Load Balancer / Reverse Proxy
  ↓
Application Service
```

### Investigation

Check:

- Reverse proxy/load balancer
- Upstream application
- Service-to-service communication
- Network connectivity
- Upstream health

---

## 503 Service Unavailable

The service is currently unavailable or unable to handle the request.

Possible causes:

- Service is down
- Service is overloaded
- Maintenance
- Failed health checks
- No healthy backend instances

### Investigation

```text
503
 ↓
Check service health
 ↓
Check running instances/processes
 ↓
Check load/capacity
 ↓
Check health checks
 ↓
Check recent deployments
```

---

## 504 Gateway Timeout

A gateway or proxy did not receive a response from an upstream service within the expected time.

Example:

```text
Client
  ↓
Gateway
  ↓
Application
  ↓
Database
       ↑
       │
    Slow response
```

Possible causes:

- Slow database query
- Slow downstream API
- Application processing taking too long
- Network latency
- Resource contention

### Investigation

```text
504
 ↓
Identify gateway/proxy
 ↓
Identify upstream service
 ↓
Check application logs
 ↓
Check dependency latency
 ↓
Check database/API performance
 ↓
Compare execution time with timeout threshold
```

---

# Practical Troubleshooting Matrix

| Code | First Question |
|---|---|
| `200` | Did the response contain the expected business result? |
| `201` | Was the resource actually created? |
| `204` | Was the successful operation expected to return no body? |
| `400` | What is invalid about the request? |
| `401` | Why can't the client authenticate? |
| `403` | Why doesn't the authenticated identity have permission? |
| `404` | Is the endpoint or requested resource missing? |
| `409` | What current state conflicts with the request? |
| `429` | Has a rate limit been exceeded? |
| `500` | What exception or server-side failure occurred? |
| `502` | Which upstream service returned an invalid response? |
| `503` | Why is the service unavailable? |
| `504` | Which upstream dependency is taking too long? |

---

# Important Support Principle

A status code is **evidence, not a complete diagnosis**.

A useful investigation combines:

```text
HTTP status
     +
Request
     +
Response body
     +
Headers
     +
Application logs
     +
Database/dependency evidence
     +
System/network information
```

The objective is to identify the failing layer and collect enough evidence to either resolve the incident or escalate it effectively.
