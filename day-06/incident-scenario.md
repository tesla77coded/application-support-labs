# Incident INC-2026-006: Checkout Failures

## Incident Overview

**Incident type:** Application / payment dependency failure
**Priority:** Urgent
**Status:** Investigated in a simulated environment
**Affected functionality:** Customer checkout and order payment


## Reported Symptoms

Customer Support reported that multiple customers could not complete checkout. After clicking "Place Order", customers received:

`Unable to process your order. Please try again later.`

The issue was reported at approximately 10:15. Available logs show failure beginning around 10:11, while the reported onset was approximately 10:00.


## System Architecture

Customer
    -> Order API
    -> Payment Service
    -> Payment Gateway
    -> Fraud-Check Service


## Initial Monitoring Evidence

| Metric | Observed value |
| --- | ---: |
| Order API HTTP 5xx rate | 18% |
| Order API average latency | 420 ms |
| Order API CPU | 42% |
| Order API Memory | 61% |
| Database Connection | 72 / 100 |
| Payment Service HTTP 5xx rate | 16% |
| Payment Service average latency | 4.8 sec |
| Payment Gateway average latency | 7.2 sec |
| Payment Gateway HTTP 5xx rate | 21% |
| Payment Gateway timeout rate | 19% |


The Order API and Payment Service health endpoints returned HTTP 200.
However, successful health checks did not establish that their downstream transaction flows were functioning correctly.


## Initial Order API Evidence

The application logs recorded payment-service failures, including an upstream HTTP 502 and a payment request timeout. The Order API subsequently returned HTTP 500 for the affected request.


## Investigation Goal

Trace the failure across service boundaries, identify the supported technical cause, distinguish it from the unconfirmed underlying deployment failure, and recommend safe recovery and prevention steps.


## Environment Note

This is a simulated incident investigation for learning and portfolio demonstration. The logs, metrics, services, and certificate details are scenario evidence, not production telemetry.
