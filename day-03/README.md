# Day 3 — HTTP, REST APIs and API Troubleshooting

## Overview

Day 3 focused on using HTTP and REST APIs from an Application Support perspective.

The goal was not simply to memorize HTTP methods and status codes, but to learn how to **reproduce API problems, isolate the failing layer, collect evidence, and escalate incidents effectively**.

---

## Topics Covered

### HTTP

- HTTP request/response structure
- Request methods
- Request and response headers
- Request and response bodies
- `Content-Type`
- `Accept`
- `Authorization`
- HTTP status codes

### REST APIs

- REST resources
- API endpoints
- HTTP methods
- Path parameters
- Query parameters
- API contracts
- Authentication
- Authorization
- Request validation
- Downstream dependencies

### API Troubleshooting

- Reproducing API failures
- Interpreting status codes
- Inspecting response bodies
- Reading application logs
- Correlating requests using request IDs
- Investigating database/API dependencies
- Distinguishing symptoms from root causes
- Escalating incidents with technical evidence

### curl

Practiced using `curl` to:

- Make GET requests
- Make POST requests
- Inspect response headers
- Enable verbose output
- Add custom headers
- Send bearer tokens
- Send JSON request bodies
- Test query parameters
- Measure API response time

---

## Important HTTP Status Codes

| Code | Meaning | Typical Support Investigation |
|---|---|---|
| `200` | OK | Verify response and business result |
| `201` | Created | Verify resource creation |
| `204` | No Content | Successful operation with no response body |
| `400` | Bad Request | Request structure/validation |
| `401` | Unauthorized | Authentication |
| `403` | Forbidden | Authorization/permissions |
| `404` | Not Found | Endpoint/resource |
| `409` | Conflict | Resource/state conflict |
| `429` | Too Many Requests | Rate limiting |
| `500` | Internal Server Error | Application/server |
| `502` | Bad Gateway | Upstream response |
| `503` | Service Unavailable | Service availability/capacity |
| `504` | Gateway Timeout | Upstream latency/timeout |

A status code narrows the investigation but does not automatically identify the root cause.

---

## Troubleshooting Workflow

The practical API troubleshooting flow used during Day 3 was:

```text
Reproduce
   ↓
Check HTTP response
   ↓
Check authentication
   ↓
Check authorization
   ↓
Validate endpoint and parameters
   ↓
Inspect request/response
   ↓
Check application logs
   ↓
Identify dependencies
   ↓
Investigate database/external services
   ↓
Collect evidence
   ↓
Escalate if required
```

The key principle is to determine **how far the request successfully progressed** before failing.

---

## Practical Incident

### INC-2026-003 — Order Retrieval API Timeout

A customer was unable to retrieve order `5005`.

The investigation began with:

```bash
curl -i https://api.shop.example.com/api/orders/5005
```

The API returned:

```text
401 Unauthorized
```

A valid bearer token was then supplied.

The request returned:

```text
504 Gateway Timeout
```

Application logs showed:

```text
Authentication successful
Database query started
Database query timeout
Failed to fetch order
Upstream dependency timeout
```

Further investigation showed:

```text
Database CPU:             94%
Active connections:       198/200
Long-running queries:     17
Normal query time:        <100 ms
Current query time:       40–50 seconds
```

A TCP connectivity check to the database succeeded.

### Assessment

The evidence strongly indicated database performance/resource contention.

However, the exact root cause was not claimed without sufficient evidence.

The incident was escalated for investigation of:

- Long-running queries
- Query execution plans
- Indexes
- Lock contention
- Connection usage
- Recent changes

See [`incidents/INC-2026-003.md`](./incidents/INC-2026-003.md) for the complete investigation.

---

## Tools Used

### curl

Used for API reproduction and troubleshooting.

Examples:

```bash
curl -i https://api.example.com/api/orders/5005
```

```bash
curl -v https://api.example.com/api/orders/5005
```

```bash
curl -i \
  -H "Authorization: Bearer <token>" \
  https://api.example.com/api/orders/5005
```

```bash
curl -s -o /dev/null \
  -w "HTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  https://api.example.com/api/orders/5005
```

### Linux Networking

Used:

```bash
nc -vz db-prod-01 5432
```

to test basic TCP connectivity to the database.

### Logs

Used request IDs, timestamps, user IDs, and resource IDs to correlate API requests with application events.

---

## Portfolio Files

```text
day-03/
├── README.md
├── http/
│   ├── request-response.md
│   └── status-codes.md
├── api/
│   └── rest-api-troubleshooting.md
├── curl/
│   └── commands.md
└── incidents/
    └── INC-2026-003.md
```

### File Purpose

| File | Purpose |
|---|---|
| `http/request-response.md` | HTTP request and response fundamentals |
| `http/status-codes.md` | HTTP status code troubleshooting |
| `api/rest-api-troubleshooting.md` | REST API investigation methodology |
| `curl/commands.md` | Practical API testing with curl |
| `incidents/INC-2026-003.md` | End-to-end API incident investigation |

---

## Key Takeaways

By the end of Day 3, the main support skills practiced were:

- Reading HTTP requests and responses
- Understanding API authentication and authorization
- Troubleshooting REST endpoints
- Using `curl` to reproduce issues
- Interpreting HTTP status codes
- Correlating API failures with application logs
- Investigating downstream dependencies
- Using network checks to eliminate basic connectivity problems
- Separating confirmed facts from hypotheses
- Writing evidence-based incident escalations

The main lesson from Day 3:

> **Don't stop at the error message. Trace the request, gather evidence, identify where it failed, and only then form a hypothesis about the cause.**
