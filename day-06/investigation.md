# Incident Investigation

## 1. Initial Assessment

Multiple customers reported checkout failures. The Order API had an HTTP 5xx rate of 18%, indicating a significant failure rate.

The available evidence did not establish that every customer or every order request was affected.

CPU, meomry, disk and database connection metrics did not initially indicate an obvious resource-exhaustion problem.


## 2. Investigation Findings

### Order API

The logs showed that order creation failed after the application attempted to call the Payment Service.

Observed outcomes included:
- An upstream HTTP 502 response.
- A payment request timeout.
- HTTP 500 response from the Order API.


### Payment Service

The health endpoint returned HTTP 200, but monitoring showed an elevated 5xx rate and average latency of 4.8 seconds, comapred with a normal latency of approximately 180 milliseconds.

The logs showed request to the Payment Gateway timing out and returning HTTP 504.


### Payment Gateway

Monitoring showed an average latency of 7.2 seconds, compared with a normal latency of approximately 250 milliseconds.

The gateway logs showed connection timeouts when attempting to contanct Fraud-Check Service.


## Fraud-Check Service

The health endpoint returned HTTP 200, and its CPU, memory, latency, and application-level eroor metrics appeared normal.

However, its logs contained repeated TLS handshake failures with certificate verification errors.


### Certificate Investigation

The certificate presented by the Fraud-Check Service had these validity dates:

- Not Before: 1 September 2026
- Not After: 7 October 2026

The simulated incident occured on 8 October 2026, so the observed certificate had expired.

Deployment history showed a certificate deployment on 7 October 20206 at 23:42.



## 3. Evidence-Based Conclusion

The expired certificate explains the certificate verification failures observed during TLS negotiation. These failures prevented successful secure communication between the Payment Gateway and the Fraud-Check Service.

The resulting downstream failures propogated through the Payment Gateway and Payment Service to the Order API, causing checkout failures.

The evidence does not establish exactly why the certificate renewal or deployment process left an expired certificate in use. That requires further investigation by the service owner.


## Verification Required After Recovery

1. Confirm that the Fraud-Check Service presents a valid certificate.
2. Verify certificate hostname, trust chain, and validity dates.
3. Test TLS connectivity from the Payment Gateway to the Fraud-Check Service.
4. Verify successful fraud checks and payment transactions.
5. Confirm that Payment Service timeouts and 5xx rates return toward their normal baseline.
6. Confirm that Order API errors and checkout failures have subsided.


## 5. Escalation

Escalate to the Fraud-Check service owner with the certificate details, TLS errors, deployment timestamps, and downstream impact.

The payment and order service owners should remain involved until end-to-end transaction processing is verified.
