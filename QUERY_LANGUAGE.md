# D-MART Query Language

This document provides a comprehensive guide to querying data in D-MART. The platform supports a unified query interface that works across both its persistence backends: File System (via Redis/RediSearch) and SQL databases.

## Overview

Querying in D-MART is primarily done via JSON payloads sent to the backend API (e.g., `/api/v1/search` or similar endpoints depending on implementation). The core object responsible for defining a query is the `Query` model.

The query engine supports:
- **Full-Text Search:** Search across multiple fields.
- **Field-Specific Filtering:** Precise matching on structured data.
- **Boolean Logic:** AND, OR, NOT operations.
- **Range Queries:** Numeric and Date ranges.
- **Aggregations:** Grouping, counting, summing, etc.
- **Joins:** Application-level joins across resources.
- **Post-Processing:** Powerful transformations using `jq`.

---

## The Query Object

A query request is a JSON object with the following structure:

```json
{
  "space_name": "management",       // Required: The space to search within
  "subpath": "/users",              // Required: The folder/path to search within
  "type": "search",                 // Default: "search". Can be "aggregation", "history", etc.

  "search": "@field:value",         // The main search string (see Syntax below)

  "filter_types": ["user"],         // Limit results to specific resource types
  "filter_tags": ["admin"],         // Limit results to specific tags
  "filter_shortnames": ["123"],     // Limit results to specific IDs
  "from_date": "2023-01-01T00:00:00", // Start date filter (created_at)
  "to_date": "2023-12-31T23:59:59",   // End date filter (created_at)

  "sort_by": "created_at",          // Field to sort by
  "sort_type": "descending",        // "ascending" or "descending"

  "limit": 10,                      // Max number of results (pagination)
  "offset": 0,                      // Number of results to skip (pagination)

  "retrieve_json_payload": true,    // Whether to return the full JSON body
  "retrieve_attachments": false,    // Whether to fetch associated attachments

  "aggregation_data": { ... },      // Aggregation configuration (see below)
  "join": [ ... ],                  // Join configuration (see below)
  "jq_filter": ".records[] | .shortname" // Post-processing filter
}
```

---

## Search Syntax

The `search` field accepts a string that follows a specific syntax, largely compatible with RediSearch.

### Basic Text Search
To perform a full-text search across indexed fields (like `shortname`, `displayname`, `description`, `tags`, etc.), simply provide the terms:

```
hello world
```
This finds records containing both "hello" **AND** "world".

### Field-Specific Search (`@field:value`)
To search within a specific field, use the `@` prefix:

```
@status:active
```

For fields nested inside the JSON payload, use the dot notation (automatically mapped):
```
@payload.body.email:john@example.com
```

### Boolean Logic
- **AND:** Implicitly applied when terms are separated by spaces.
  ```
  @status:active @category:books
  ```
  (Status is active AND Category is books)

- **OR:** Use the pipe `|` character.
  ```
  @status:active|pending
  ```
  (Status is active OR pending)

  You can also group values with parentheses:
  ```
  @status:(active|pending)
  ```

- **NOT:** Use the minus `-` prefix.
  ```
  -@status:archived
  ```
  (Status is NOT archived)

### Ranges (`[min max]`)
Ranges are supported for numeric and date fields. The syntax uses square brackets `[]` with values separated by a space or comma.

- **Numeric Range:**
  ```
  @price:[10 100]
  ```
  (Price is between 10 and 100, inclusive)

- **Date Range:**
  Supported formats include ISO 8601 (e.g., `YYYY-MM-DD`, `YYYY-MM-DDTHH:MM:SS`).
  ```
  @created_at:[2023-01-01 2023-12-31]
  ```

### Exact Match vs Partial
- **Exact:** `@field:value` usually implies an exact match for keyword fields.
- **Prefix:** Wildcards `*` are supported for prefix matching in text fields.
  ```
  @name:John*
  ```

---

## Filtering

In addition to the `search` string, specific fields provide optimized filtering:

| Field | Description | Example |
|---|---|---|
| `filter_types` | List of resource types to include. | `["user", "role"]` |
| `filter_tags` | List of tags. A record must have at least one matching tag. | `["urgent", "bug"]` |
| `filter_shortnames` | List of specific IDs (shortnames) to retrieve. | `["u-123", "u-456"]` |
| `from_date` | Filter records created after this date. | `"2023-01-01"` |
| `to_date` | Filter records created before this date. | `"2023-12-31"` |

---

## Aggregations

Aggregations allow you to group data and calculate metrics (counts, sums, averages). To perform an aggregation, set `type` to `"aggregation"` and provide `aggregation_data`.

### Structure

```json
"aggregation_data": {
  "group_by": ["@field1", "@field2"],  // Fields to group by
  "reducers": [                        // Calculations to perform
    {
      "reducer_name": "count",         // Function: count, sum, avg, min, max
      "alias": "total_count",          // Name for the result field
      "args": []                       // Arguments (e.g., field name for sum/avg)
    }
  ],
  "load": ["@field1", "@total_count"]  // Fields to include in the output
}
```

### Supported Reducers
- `count`: Count records.
- `sum`: Sum a numeric field.
- `avg`: Calculate average of a numeric field.
- `min` / `max`: Find minimum or maximum values.
- `group_concat` (SQL) / `tolist` (Redis): Concatenate values into a list/string.

---

## Joins

D-MART supports application-level joins, allowing you to combine data from different resources (even across spaces) in a single request.

### Structure

```json
"join": [
  {
    "alias": "orders",          // The field name where joined data will appear
    "join_on": "id:user_id",    // LocalField:RemoteField mapping
    "query": {                  // The query to fetch the related data
      "space_name": "commerce",
      "subpath": "/orders",
      "type": "search"
    }
  }
]
```

### How it works
1. The main query executes and retrieves a list of records (e.g., Users).
2. For each user, the system extracts the value of the "Local Field" (e.g., `id`).
3. It executes the `query` defined in the join block, adding a filter: `@RemoteField:extracted_value`.
4. The matching records (Orders) are attached to the User record under the `attributes.join.orders` field.

---

## Post-Processing (`jq`)

For advanced data transformation, you can apply a [jq](https://jqlang.github.io/jq/) filter to the results before they are returned. This runs on the server side.

```json
"jq_filter": ".records[] | {name: .attributes.payload.body.name, email: .attributes.payload.body.email}"
```

---

## Examples

### 1. Simple User Search
Find users created in 2023 with "active" status.

```json
{
  "space_name": "management",
  "subpath": "/users",
  "type": "search",
  "search": "@status:active @created_at:[2023-01-01 2023-12-31]",
  "filter_types": ["user"],
  "retrieve_json_payload": true
}
```

### 2. Aggregation: Count Users by City
Group users by their city and count them.

```json
{
  "space_name": "management",
  "subpath": "/users",
  "type": "aggregation",
  "aggregation_data": {
    "group_by": ["@payload.body.city"],
    "reducers": [
      { "reducer_name": "count", "alias": "user_count", "args": [] }
    ],
    "load": ["@payload.body.city", "@user_count"]
  }
}
```

### 3. Join: Users with their Roles
Fetch users and join their role details.

```json
{
  "space_name": "management",
  "subpath": "/users",
  "type": "search",
  "join": [
    {
      "alias": "role_details",
      "join_on": "roles[]:shortname",
      "query": {
        "space_name": "management",
        "subpath": "/roles",
        "type": "search"
      }
    }
  ]
}
```
*Note: `roles[]` indicates that the local field `roles` is an array of IDs.*
