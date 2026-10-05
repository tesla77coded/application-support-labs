# Query Parameter Request

## Purpose

Test filtering a collection using a query parameter.

## Request

```http
GET https://jsonplaceholder.typicode.com/users?username=Bret
```

## Result

**Status:** `200 OK`

**Users returned:** `1`

The response contained the user with the username `Bret`.

## Query Parameter

```text
/users?username=Bret
       └────────────┘
       query parameter
```

The query parameter is:

```text
username=Bret
```

For this API, the parameter is used to filter the users collection by username.

## Comparison

Without the query parameter:

```http
GET /users
```

The API returned the users collection.

With the query parameter:

```http
GET /users?username=Bret
```

The API returned the matching user.

## Key Observation

The meaning of a query parameter is determined by the API's implementation. The parameter does not inherently mean "filter"; the backend defines how it is handled.
