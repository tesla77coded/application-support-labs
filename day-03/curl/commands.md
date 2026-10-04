# curl Commands for API Troubleshooting

## Overview

`curl` is a command-line tool used to make HTTP requests.

For Application Support and Technical Support, `curl` is useful for:

- Reproducing API issues
- Testing endpoints
- Inspecting HTTP status codes
- Inspecting request and response headers
- Sending authentication credentials
- Sending JSON request bodies
- Testing query parameters
- Investigating API connectivity and behavior

The goal is not to memorize every `curl` option, but to be comfortable using it to investigate API problems.

---

## 1. Basic GET Request

```bash
curl https://httpbin.org/get
```

This sends a basic:

```text
GET /get
```

request.

The response body is printed to the terminal.

---

## 2. Include Response Headers

Use `-i`:

```bash
curl -i https://httpbin.org/get
```

This displays both:

- Response headers
- Response body

Example:

```text
HTTP/2 200
content-type: application/json
content-length: ...

{
  ...
}
```

### Support Use Case

Useful when you need to quickly inspect:

- HTTP status code
- `Content-Type`
- Cache headers
- Server information
- Other response headers

---

## 3. Verbose Mode

Use `-v`:

```bash
curl -v https://httpbin.org/get
```

Verbose mode provides detailed information about the request and connection.

The output uses symbols to distinguish different information.

### `>` — Client to Server

Example:

```text
> GET /get HTTP/2
> Host: httpbin.org
> User-Agent: curl/8.22.0
> Accept: */*
```

These are request details sent by `curl`.

### `<` — Server to Client

Example:

```text
< HTTP/2 200
< content-type: application/json
```

These are response details received from the server.

### `*` — curl Diagnostic Information

Example:

```text
* Connected to httpbin.org
* Request completely sent off
```

These messages describe connection and `curl` behavior.

### Support Use Case

Use `-v` when you need more detail about:

- DNS resolution
- TCP/TLS connection
- Request transmission
- Response headers
- Connection problems

---

## 4. Add a Custom Request Header

Use `-H`:

```bash
curl -i \
  -H "X-Support-Test: Day-3" \
  https://httpbin.org/get
```

This adds:

```http
X-Support-Test: Day-3
```

to the request.

Multiple headers can be added:

```bash
curl -i \
  -H "X-Support-Test: Day-3" \
  -H "Accept: application/json" \
  https://httpbin.org/get
```

### Support Use Case

Custom headers are commonly used for:

- Authentication
- Content negotiation
- Correlation/request IDs
- Feature flags
- API-specific headers
- Testing

---

## 5. Send an Authorization Header

Bearer-token authentication commonly uses:

```bash
curl -i \
  -H "Authorization: Bearer <token>" \
  https://api.example.com/api/orders/5005
```

The request contains:

```http
Authorization: Bearer <token>
```

If the token is missing or invalid, the API may return:

```text
401 Unauthorized
```

If authentication succeeds but the user lacks permission, the API may return:

```text
403 Forbidden
```

---

## 6. GET Request with Query Parameters

Example:

```bash
curl -i \
  "https://api.example.com/api/orders?status=pending&limit=20"
```

The request contains:

```text
status=pending
limit=20
```

Query parameters are useful for:

- Filtering
- Searching
- Pagination
- Sorting
- Optional request behavior

Always quote URLs containing query parameters:

```bash
"https://api.example.com/api/orders?status=pending&limit=20"
```

This avoids shell interpretation problems with special characters such as `&`.

---

## 7. POST Request

Use `-X POST` to explicitly specify the HTTP method:

```bash
curl -i \
  -X POST \
  https://httpbin.org/post
```

A POST request commonly sends data in the request body.

---

## 8. Send Form/Data with `-d`

The `-d` option sends request data.

Example:

```bash
curl -i \
  -X POST \
  -d "name=Rahul" \
  https://httpbin.org/post
```

For API testing, JSON is commonly used instead.

---

## 9. Send JSON

Example:

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"Rahul","email":"rahul@example.com"}' \
  https://httpbin.org/post
```

The important parts are:

```text
-X POST
```

Specifies the HTTP method.

```text
-H "Content-Type: application/json"
```

Tells the server that the request body is intended to be JSON.

```text
-d '{...}'
```

Sends the JSON request body.

---

## 10. Example of an API Contract Investigation

Suppose an API expects:

```json
{
  "name": "Rahul",
  "email": "rahul@example.com",
  "password": "example123"
}
```

A support engineer could reproduce the request with:

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul",
    "email": "rahul@example.com",
    "password": "example123"
  }' \
  https://api.example.com/api/users
```

If the API returns:

```text
400 Bad Request
```

investigate:

- Required fields
- Field names
- Data types
- JSON syntax
- Validation rules
- API documentation

---

## 11. Testing an Authentication Failure

Request without credentials:

```bash
curl -i \
  https://api.example.com/api/orders/5005
```

Possible response:

```text
HTTP/2 401 Unauthorized
```

Retry with authentication:

```bash
curl -i \
  -H "Authorization: Bearer <token>" \
  https://api.example.com/api/orders/5005
```

If the result changes from:

```text
401
```

to:

```text
504
```

that is useful evidence.

It means authentication was blocking the first request, but after authentication succeeded, the request progressed further and encountered another problem.

---

## 12. Testing a Specific API Incident

Example:

```bash
curl -i \
  -H "Authorization: Bearer <token>" \
  -H "Accept: application/json" \
  https://api.shop.example.com/api/orders/5005
```

Possible response:

```text
HTTP/2 504 Gateway Timeout
```

At this point, investigate:

1. API/application logs
2. Request ID
3. Upstream services
4. Database performance
5. Network connectivity to dependencies
6. Timeouts and resource saturation

`curl` has reproduced the issue, but it does not by itself identify the root cause.

---

## 13. Useful curl Options

| Option | Purpose |
|---|---|
| `-i` | Include response headers |
| `-v` | Verbose request/connection information |
| `-X` | Specify HTTP method |
| `-H` | Add request header |
| `-d` | Send request data/body |
| `-s` | Silent mode |
| `-o` | Write output to a file |
| `-w` | Display custom response information |
| `-L` | Follow redirects |
| `-u` | Send basic authentication credentials |

---

## 14. Timing an API Request

The `-w` option can display request timing information.

Example:

```bash
curl -s -o /dev/null \
  -w "HTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  https://api.example.com/api/orders/5005
```

Example output:

```text
HTTP Status: 504
Time: 40.82s
```

This can provide useful evidence when investigating slow APIs or timeout incidents.

For example, if an endpoint normally responds in under one second but currently takes 40 seconds, that is worth correlating with application and dependency logs.

---

## 15. Save a Response to a File

Use `-o`:

```bash
curl -o response.json \
  https://api.example.com/api/orders/5005
```

This writes the response body to:

```text
response.json
```

This can be useful when the response is large or needs to be reviewed separately.

---

## 16. Support Troubleshooting Pattern

A practical sequence is:

```bash
# 1. Basic request
curl -i https://api.example.com/api/orders/5005

# 2. Add authentication
curl -i \
  -H "Authorization: Bearer <token>" \
  https://api.example.com/api/orders/5005

# 3. Add expected response format
curl -i \
  -H "Authorization: Bearer <token>" \
  -H "Accept: application/json" \
  https://api.example.com/api/orders/5005

# 4. If more connection/request detail is needed
curl -v \
  -H "Authorization: Bearer <token>" \
  https://api.example.com/api/orders/5005

# 5. Measure response time
curl -s -o /dev/null \
  -w "HTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -H "Authorization: Bearer <token>" \
  https://api.example.com/api/orders/5005
```

The exact command depends on what the investigation is trying to establish.

---

## Key Support Takeaways

- `curl` is useful for reproducing API issues independently of the application's UI.
- `-i` shows response headers.
- `-v` provides detailed request and connection information.
- `-H` adds request headers.
- `-X` specifies the HTTP method.
- `-d` sends request data.
- `Content-Type` describes the request body format.
- `Authorization` can be used to test authenticated API access.
- Query parameters should be included correctly and URLs containing `&` should be quoted.
- `curl` can measure response time and provide evidence for timeout/latency incidents.
- Reproducing an issue with `curl` is only the beginning of troubleshooting; logs, databases, dependencies, and monitoring may still be required to identify the cause.
