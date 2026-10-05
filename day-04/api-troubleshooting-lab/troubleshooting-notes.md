# API Troubleshooting Notes

## HTTP Request Anatomy

An HTTP request can contain:

- Method
- URL
- Path parameters
- Query parameters
- Headers
- Request body

Example:

```http
POST /api/users/123?include=orders
Content-Type: application/json
Authorization: Bearer <token>
```

## HTTP Response Anatomy

An HTTP response contains:

- Status code
- Response headers
- Response body
- Response timing

---

## Path Parameters

Path parameters identify a specific resource.

Example:

```text
/users/123
```

Here `123` identifies the requested user.

---

## Query Parameters

Query parameters modify or filter a request.

Example:

```text
/users?username=Bret
```

In the API tested during this lab, `username=Bret` filtered the users collection.

The meaning of a query parameter is determined by the API's implementation.

---

## Important Headers

### Authorization

Used to provide authentication credentials.

Example:

```text
Authorization: Bearer <token>
```

### Content-Type

Describes the format of the request body.

Example:

```text
Content-Type: application/json
```

### Accept

Indicates the response format preferred by the client.

Example:

```text
Accept: application/json
```

### User-Agent

Identifies the client making the request.

Example:

```text
User-Agent: PostmanRuntime/2.10.1
```

---

## Authentication vs Authorization

### 401 Unauthorized

Usually indicates an authentication problem.

Mental model:

```text
401 → "Who are you?"
```

Common causes:

- Missing credentials
- Invalid credentials
- Expired token
- Invalid authentication token

### 403 Forbidden

Usually indicates an authorization problem.

Mental model:

```text
403 → "I know who you are, but you're not allowed."
```

Common causes:

- Missing role
- Missing permission
- Resource access restrictions

---

## Important Status Codes

| Status | Meaning | Typical Investigation |
|---|---|---|
| 200 | OK | Request succeeded |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Request syntax/data/API contract |
| 401 | Unauthorized | Authentication |
| 403 | Forbidden | Authorization |
| 404 | Not Found | Resource/route |
| 409 | Conflict | Resource/state conflict |
| 429 | Too Many Requests | Rate limiting |
| 500 | Internal Server Error | Application/server failure |
| 502 | Bad Gateway | Upstream connection/response problem |
| 503 | Service Unavailable | Service unavailable/overloaded |
| 504 | Gateway Timeout | Upstream response exceeded timeout |

---

# Troubleshooting Patterns

## 400

Start with the request.

Check:

- JSON syntax
- Required fields
- Field names
- Data types
- Parameter values
- API documentation

Do not immediately assume the server is broken.

---

## 401

Check:

- Is authentication required?
- Is the authentication header present?
- Is the token valid?
- Has the token expired?
- Is the correct authentication mechanism being used?

Never record real tokens in incident tickets.

---

## 403

Check:

- User role
- User permissions
- Required endpoint permissions
- Resource-level restrictions
- Authorization configuration

Authentication may be completely valid while authorization fails.

---

## 404

Determine whether the missing item is:

- The endpoint itself
- A resource requested through an existing endpoint

For example:

```text
/users/1 → 200
/users/99999 → 404
```

This suggests the endpoint exists but the requested resource does not.

---

## 500

Start with application evidence.

Typical process:

```text
500
 ↓
Application logs
 ↓
Identify failing component
 ↓
Investigate dependency
 ↓
Database / external service / application logic
```

Do not immediately assume the database is responsible.

---

## 502

Think:

```text
Gateway
   ↓
Upstream
   ✕
```

Investigate:

- Upstream service health
- Connectivity
- Ports
- Service availability
- Gateway configuration
- Recent deployments

---

## 504

Think:

```text
Gateway
   ↓
Upstream
   ↓
Processing...
   ↓
Timeout
```

Investigate:

- Upstream processing time
- Application performance
- Database query performance
- Resource utilization
- Locks/contention
- Downstream dependencies
- Recent changes

A timeout does not automatically mean the timeout value should simply be increased.

---

# Evidence-Driven Troubleshooting

A key principle from this lab:

> Do not confuse an observation with a confirmed root cause.

Example:

```text
Observed:
Database connection timeout
```

This does not automatically prove:

```text
Root cause:
Slow SQL query
```

The connection timeout could instead be caused by:

- Connection pool exhaustion
- Database connection limits
- Network failure
- Database overload
- Database availability issue

The correct approach is:

```text
Observation
    ↓
Hypothesis
    ↓
Test
    ↓
Evidence
    ↓
Conclusion
```

---

# Escalation Principle

Escalation should include evidence rather than simply stating that something is broken.

Useful escalation information includes:

- Incident ID
- Timestamp
- Endpoint
- HTTP status
- Request details
- Relevant logs
- Error messages
- Tests performed
- Results
- Suspected failing component
- Impact/scope
- Recent relevant changes

Never include:

- Passwords
- API keys
- Access tokens
- Secrets
- Unnecessary sensitive customer data
