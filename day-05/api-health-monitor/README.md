# API Health Monitor

A lightweight API health monitoring utility built as part of an Application Support troubleshooting lab.

The project monitors an HTTP endpoint for availability, HTTP errors, response latency, timeouts, and connection failures. It records health-check results in a persistent log and includes automated pytest tests for the main monitoring scenarios.

The purpose of this project is to demonstrate practical Application Support concepts such as health checks, monitoring signals, threshold-based evaluation, incident evidence collection, logging, and automated validation.

---

## Objectives

This project demonstrates the following Application Support capabilities:

- API availability monitoring
- HTTP status monitoring
- Response-time monitoring
- Timeout detection
- Connection-failure detection
- Threshold-based health evaluation
- Persistent health-check logging
- Automated testing with pytest
- Basic incident investigation and troubleshooting
- Separation of monitoring configuration from monitoring logic

---

## Architecture

```text
                    API Endpoint
                         │
                         │ HTTP GET
                         ▼
                ┌─────────────────┐
                │  Health Monitor │
                └────────┬────────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
           HTTP       Latency    Connectivity
           Status     Measurement   Result
              │          │          │
              └──────────┼──────────┘
                         ▼
                  Health Evaluation
                         │
                 ┌───────┴────────┐
                 ▼                ▼
              HEALTHY          UNHEALTHY
                 │                │
                 └───────┬────────┘
                         ▼
                  Persistent Log
```

---

## Health Criteria

The monitor currently considers an endpoint **HEALTHY** when:

```text
HTTP status = 200
AND
response latency < 2 seconds
```

The endpoint is considered **UNHEALTHY** when any of the following occurs:

- HTTP status is not `200`
- Response latency is greater than or equal to the configured threshold
- The request times out
- A connection/request error occurs

These thresholds are configurable and are intended for demonstration purposes.

They should not be treated as universal production thresholds.

---

## Monitoring Configuration

Configuration is maintained separately from the monitoring logic in `config.py`.

Current configuration:

```text
URL
TIMEOUT
LATENCY_THRESHOLD
CHECK_INTERVAL
```

Example:

```python
URL = "https://httpbin.org/"
TIMEOUT = 5
LATENCY_THRESHOLD = 2.0
CHECK_INTERVAL = 10
```

This separation allows the monitored endpoint and monitoring thresholds to be changed without modifying the core health-check logic.

---

## Monitored Conditions

### 1. Healthy API

Example:

```text
HTTP: 200
Latency: 0.127s
```

Result:

```text
HEALTHY
```

---

### 2. HTTP Error

Example:

```text
HTTP: 500
```

Result:

```text
UNHEALTHY
Reason: HTTP 500
```

The application responded, but returned a server-side error.

---

### 3. Slow Response

Example:

```text
HTTP: 200
Latency: 3.2s
```

Result:

```text
UNHEALTHY
Reason: Response too slow
```

The service is reachable and technically responding successfully, but its performance has degraded beyond the configured threshold.

This demonstrates that:

> HTTP 200 does not necessarily mean the application is healthy.

---

### 4. Request Timeout

Example:

```text
No response within configured timeout
```

Result:

```text
UNHEALTHY
Reason: Request timed out
```

No HTTP response is available because the request did not complete within the allowed time.

---

### 5. Connection Failure

Example:

```text
Unable to establish a connection
```

Result:

```text
UNHEALTHY
```

This is different from an HTTP error because the application did not successfully return an HTTP response.

---

## Logging

Health-check results are written to `health.log`.

Example:

```text
2026-10-06 16:55:59,636 | INFO | HEALTHY | HTTP: 200 | Latency: 0.062s | Reason: None

2026-10-06 16:56:13,128 | INFO | HEALTHY | HTTP: 200 | Latency: 0.043s | Reason: None
```

Unhealthy checks are recorded at the `ERROR` level.

Example:

```text
2026-10-06 17:10:21,542 | ERROR | UNHEALTHY | HTTP: 500 | Latency: 0.421s | Reason: HTTP 500
```

The log provides a basic historical record that can be used during incident investigation.

For example, a support engineer can determine when an endpoint transitioned from healthy to unhealthy and correlate that time with application, database, or infrastructure logs.

---

## Troubleshooting an UNHEALTHY Result

An unhealthy result should be treated as an **investigation trigger**, not automatically as a diagnosis.

### HTTP 4xx

If the monitor receives a `4xx` response:

1. Confirm the endpoint being monitored.
2. Check whether authentication or authorization is required.
3. Verify request parameters and headers.
4. Determine whether the endpoint itself has changed.
5. Check application/API logs if necessary.

A `4xx` generally indicates that the server received the request but considers the request invalid or unauthorized.

---

### HTTP 5xx

If the monitor receives a `5xx` response:

1. Confirm the endpoint is reachable.
2. Check application logs around the same timestamp.
3. Identify the operation that failed.
4. Check database or external-service dependencies.
5. Check for recent deployments or configuration changes.
6. Determine whether the issue affects one endpoint or multiple endpoints.
7. Document the evidence.
8. Escalate according to the support process if the issue requires another team.

A `5xx` response indicates a server-side failure, but does not by itself identify the root cause.

---

### Timeout

If the monitor reports a timeout:

1. Confirm whether the endpoint is reachable.
2. Check current API latency.
3. Check application logs for slow requests or dependency timeouts.
4. Check database connectivity and query performance.
5. Check external API/dependency latency.
6. Investigate network connectivity to the affected dependency.
7. Compare the current behavior against the normal baseline.

Possible causes include:

- Slow application processing
- Slow database queries
- Database connection problems
- External dependency delays
- Network problems
- Resource exhaustion

---

### Connection Failure

If the monitor cannot establish a connection:

1. Verify DNS resolution.
2. Verify the destination host and port.
3. Check whether the target service is running.
4. Check network connectivity.
5. Check firewall or connectivity restrictions where applicable.
6. Review relevant application or infrastructure logs.

The important distinction is:

```text
Connection failure
        ≠
HTTP error
```

A connection failure means an HTTP response was not successfully obtained.

---

### Slow HTTP 200 Response

If the monitor receives `HTTP 200` but exceeds the latency threshold:

1. Confirm that the latency increase is consistent.
2. Check application logs.
3. Investigate slow database queries.
4. Check external dependency latency.
5. Check resource utilization.
6. Compare the current latency with the normal baseline.
7. Investigate recent changes.

The service may be available while still being operationally unhealthy.

---

## Example Incident Investigation

### Incident

```text
INC-2026-002
```

### Symptom

The API health monitor reports:

```text
UNHEALTHY
HTTP: 500
Latency: 0.421s
Reason: HTTP 500
```

### Initial Assessment

The endpoint is reachable because an HTTP response was received.

The problem appears to be a server-side application failure rather than a basic connectivity failure.

### Investigation

A support engineer would:

```text
Health Monitor
      ↓
Confirm HTTP 500
      ↓
Check application logs
      ↓
Identify failing operation
      ↓
Check database / external dependency
      ↓
Check recent changes
      ↓
Determine impact
      ↓
Document evidence
      ↓
Resolve or escalate
```

### Example evidence

```text
Health Monitor:
HTTP 500

Application Log:
Database query failed

Database:
Connection timeout

Timeline:
14:31 — API healthy
14:32 — HTTP 500 begins
14:32 — Database timeout appears in logs
```

### Preliminary Finding

The API is reachable, but report generation is failing because the application is experiencing a database connectivity problem.

### Next Action

Follow the organization's incident procedure and escalate to the appropriate database/infrastructure team if the issue cannot be resolved at the application's support level.

---

## Testing

The project uses `pytest` to validate the monitoring logic.

The test suite covers:

- Successful HTTP `200` response
- HTTP `400`
- HTTP `401`
- HTTP `403`
- HTTP `404`
- HTTP `500`
- HTTP `502`
- HTTP `503`
- HTTP `504`
- Request timeout
- Connection failure
- Slow `HTTP 200` response

The tests use mocking rather than making real external network requests.

This makes the tests:

- Faster
- Repeatable
- Independent of external service availability
- Deterministic

Run the test suite with:

```bash
pytest -v
```

Expected result:

```text
12 passed
```

---

## Project Structure

```text
api-health-monitor/
│
├── monitor.py
│       Core health-check and monitoring logic
│
├── config.py
│       Monitoring configuration and thresholds
│
├── requirements.txt
│       Python dependencies
│
├── health.log
│       Persistent health-check results
│
├── README.md
│       Project documentation and troubleshooting runbook
│
└── tests/
    └── test_monitor.py
            Automated health-check tests
```

---

## Installation

Clone the repository and enter the project directory.

Create and activate a virtual environment if desired:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Monitor

Start the monitor with:

```bash
python monitor.py
```

Example output:

```text
status: HEALTHY | HTTP: 200 | Latency: 0.127s | Reason: None
```

The monitor performs checks according to the configured interval.

Stop the monitor with:

```text
Ctrl+C
```

---

## Key Application Support Concepts Demonstrated

This project demonstrates practical understanding of:

- Health checks
- Application availability
- API monitoring
- Response latency
- HTTP status monitoring
- Monitoring thresholds
- Alerts as investigation triggers
- Metrics and operational signals
- Application logs
- Dependency troubleshooting
- Evidence-driven investigation
- Incident documentation
- Automated validation
- Basic monitoring automation

---

## Limitations

This is a learning and portfolio project, not a production monitoring platform.

It currently does not provide:

- A monitoring dashboard
- Persistent metrics storage
- Distributed tracing
- Alert delivery through email, Slack, PagerDuty, etc.
- Authentication/secret management
- High-availability monitoring
- Multiple monitored services
- Production-grade scheduling
- Automatic remediation

The project intentionally focuses on the core Application Support concepts of **health checking, detection, logging, troubleshooting, and evidence collection**.

---

## What This Project Demonstrates

The primary objective is not the Python code itself.

The project demonstrates the following support workflow:

```text
Monitor
   ↓
Detect abnormal behavior
   ↓
Measure the symptom
   ↓
Classify the health state
   ↓
Record evidence
   ↓
Investigate the affected layer
   ↓
Correlate with logs/dependencies
   ↓
Document findings
   ↓
Resolve or escalate
```

This reflects the basic reasoning required when supporting applications in a production environment.
