# GET User Request

## Purpose

Test retrieving a specific user using a path parameter.

## Request

```http
GET https://jsonplaceholder.typicode.com/users/1
```

## Result

**Status:** `200 OK`

The API returned the details of user `1`.

## Path Parameter

```text
/users/1
       ↑
    user ID
```

The `1` identifies the specific user resource being requested.

## Response

The response contained a JSON object representing the requested user.

## Troubleshooting Test

A non-existent user was also tested:

```http
GET https://jsonplaceholder.typicode.com/users/99999
```

**Result:** `404 Not Found`

This demonstrated that the endpoint was available, but the requested resource did not exist.

## Key Observation

A `404` response does not necessarily mean that the endpoint itself is unavailable. The endpoint may exist while the specific resource being requested does not.
