# Day 2 — SQL & Database Troubleshooting

## Objective

Learn SQL fundamentals and apply database investigation
techniques to common Application Support incidents.

## Topics Covered

- SELECT and filtering
- ORDER BY and LIMIT
- NULL handling
- INSERT, UPDATE and DELETE
- Safe database modifications
- Aggregate functions
- GROUP BY and HAVING
- INNER JOIN
- LEFT JOIN
- Primary keys
- Foreign keys
- Indexes
- Transactions
- Database troubleshooting

## Database Model

users
  ↓
orders
  ↓
payments

## Troubleshooting Approach

Customer issue
    ↓
Identify relevant record
    ↓
Query database
    ↓
Compare related records
    ↓
Identify discrepancy
    ↓
Form hypothesis
    ↓
Investigate application/logs/API
    ↓
Document findings

## Incidents Investigated

### INC-2026-002
Successful payment but order remains pending.

### INC-2026-004
Payment record exists but remains pending.

### INC-2026-005
Order exists but corresponding payment record is missing.

## Key Support Lessons

- SQL can provide evidence during incident investigation.
- Database evidence should not automatically be treated as root cause.
- UPDATE and DELETE require careful use of WHERE.
- INNER JOIN finds matching records across tables.
- LEFT JOIN can reveal missing related records.
- A successful payment and pending order may indicate a state
  synchronization or processing issue, but further evidence is required.
- Missing database records can indicate failures earlier in the
  application/payment flow.

## Tools

- SQL
- PostgreSQL concepts
- Git/GitHub
