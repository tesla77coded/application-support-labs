# API Troubleshooting Lab

## Overview

This lab simulates real-world Application Support incidents involving REST APIs.

The objective is to practice reproducing API issues, analyzing HTTP requests and responses, identifying the likely failing component, determining root cause, and decidign whether an issue can be resolved or should be escalated.

## Tools
- Postman
- curl
- HTTP/REST APIs
- JSON
- Linux
- SQL / database troubleshooting
- Application logs

## Troubleshooting Methodology

The general investigation process used in this lab is:

1. Reproduce the issue
2. Inspect the HTTP request.
3. Inspect the HTTP response.
4. Check the status code.
5. Inspect headers and request/response body.
6. Check application logs when applicable.
7. Identify the failing componenet.
8. Form and test hypotheses.
9. Determine root cause.
10. Resolve or escalate.
11. Document evidence.


## API Concepts Practiced

- HTTP methods
- REST endpoints
- Path parameters
- Query parameters
- Request headers
- Response headers
- Request bodies
- JSON
- Authentication
- Authorization
- HTTP status codes


## Incidents Investigated

| Incident | Status | Issue |
|---|---:|---|
| INC-2026-005 | 400 | Invalid request data type |
| INC-2026-006 | 401 | Missing authentication |
| INC-2026-007 | 403 | Insufficient authorization |
| INC-2026-008 | 500 | Application/database failure |
| INC-2026-009 | 502 | Upstream connection failure |
| INC-2026-010 | 504 | Upstream timeout |


## Key Principle

Troubleshooting should be evidence-driven.

Observed behavior should be distinguished from assumption about the underlying cause.
