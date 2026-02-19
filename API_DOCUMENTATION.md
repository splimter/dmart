# DMART API Documentation

This document provides a comprehensive reference for the DMART API. It details available endpoints, data structures, and usage examples.

## Base URL

The base URL for all API requests is typically:
`http://localhost:8000` (or as configured in your environment)

## Authentication

Most endpoints require authentication using a JWT token.
- **Header**: `Authorization: Bearer <your_token>`
- **Cookie**: `auth_token=<your_token>`

## Common Data Structures

### Record
Represents a resource in the system. This is the primary object for creating or updating entities.

```json
{
  "resource_type": "content",
  "shortname": "my-article",
  "subpath": "/blog",
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "attributes": {
    "is_active": true,
    "slug": "my-article-slug",
    "displayname": { "en": "My Article" },
    "description": { "en": "A description" },
    "tags": ["news", "tech"],
    "owner_shortname": "jdoe",
    "owner_group_shortname": "editors",
    "created_at": "2023-10-01T12:00:00",
    "updated_at": "2023-10-01T12:00:00",
    "payload": {
      "content_type": "json",
      "schema_shortname": "article",
      "body": { "title": "Hello World", "content": "..." }
    },
    "acl": [
      {
        "user_shortname": "jane",
        "allowed_actions": ["view", "update"]
      }
    ],
    "relationships": [
      {
        "related_to": {
          "space_name": "data",
          "type": "user",
          "subpath": "users",
          "shortname": "jane"
        },
        "attributes": { "role": "editor" }
      }
    ]
  }
}
```

### Request
Used for batch operations (create, update, delete, etc.).

```json
{
  "space_name": "data",
  "request_type": "create",
  "records": [ ... list of Record objects ... ]
}
```

### Query
Used for searching and filtering resources.

```json
{
  "type": "search",
  "space_name": "data",
  "subpath": "/blog",
  "exact_subpath": false,
  "filter_types": ["content"],
  "filter_schema_names": ["article"],
  "filter_shortnames": [],
  "filter_tags": ["tech"],
  "search": "@title:Hello*",
  "from_date": "2023-01-01T00:00:00",
  "to_date": "2023-12-31T23:59:59",
  "exclude_fields": ["payload.body"],
  "include_fields": ["shortname", "displayname"],
  "highlight_fields": { "description.en": "<b>" },
  "sort_by": "created_at",
  "sort_type": "descending",
  "retrieve_json_payload": true,
  "retrieve_attachments": false,
  "retrieve_total": true,
  "validate_schema": true,
  "retrieve_lock_status": false,
  "jq_filter": ". | select(.attributes.is_active == true)",
  "limit": 10,
  "offset": 0,
  "aggregation_data": {
    "group_by": ["@tags"],
    "reducers": [
      { "reducer_name": "count_distinct", "alias": "count", "args": ["@shortname"] }
    ]
  },
  "join": [
    {
      "join_on": "uuid",
      "alias": "author_details",
      "query": { ... nested Query object ... }
    }
  ]
}
```

## Enums and Possible Values

### ResourceType
`user`, `group`, `folder`, `schema`, `content`, `log`, `acl`, `comment`, `media`, `data_asset`, `locator`, `relationship`, `alteration`, `history`, `space`, `permission`, `role`, `ticket`, `json`, `lock`, `post`, `reaction`, `reply`, `share`, `plugin_wrapper`, `notification`, `csv`, `jsonl`, `sqlite`, `duckdb`, `parquet`

### RequestType
`create`, `update`, `patch`, `update_acl`, `assign`, `delete`, `move`

### ContentType
`text`, `comment`, `reaction`, `markdown`, `html`, `json`, `image`, `python`, `pdf`, `audio`, `video`, `csv`, `parquet`, `jsonl`, `apk`, `duckdb`, `sqlite`

### ActionType
`query`, `view`, `update`, `create`, `delete`, `attach`, `assign`, `move`, `progress_ticket`, `lock`, `unlock`

### QueryType
`search`, `subpath`, `events`, `history`, `tags`, `random`, `spaces`, `counters`, `reports`, `aggregation`, `attachments`, `attachments_aggregation`

### SortType
`ascending`, `descending`

### TaskType
`query`

### UserType
`web`, `mobile`, `bot`

### Language
`ar` (Arabic), `en` (English), `ku` (Kurdish), `fr` (French), `tr` (Turkish)

### ConditionType
`is_active`, `own`

### ReactionType
`like`, `dislike`, `love`, `care`, `laughing`, `sad`

### LockAction
`fetch`, `lock`, `extend`, `unlock`, `cancel`

### NotificationType
`admin`, `system`

### NotificationPriority
`high`, `medium`, `low`

### PluginType
`hook`, `api`

### EventListenTime
`before`, `after`

---

## API Endpoints

### User Management (`/user`)

#### Check Existing User Fields
Checks if a user with specific fields already exists.
- **Method**: `GET /user/check-existing`
- **Query Params**:
  - `shortname`: (Optional) User shortname
  - `msisdn`: (Optional) Mobile number
  - `email`: (Optional) Email address

#### Create User
Registers a new user.
- **Method**: `POST /user/create`
- **Body**: `Record` object (wrapped in a standard request structure implicitly via `core.Record` binding)
- **Example**:
```json
{
  "resource_type": "user",
  "shortname": "jdoe",
  "subpath": "users",
  "attributes": {
    "email": "jdoe@example.com",
    "password": "StrongPassword123!",
    "displayname": { "en": "John Doe" }
  }
}
```

#### Login
Authenticates a user and returns a token.
- **Method**: `POST /user/login`
- **Body**:
```json
{
  "shortname": "jdoe",
  "password": "StrongPassword123!"
}
```
Or via OTP/Invitation:
```json
{
  "msisdn": "1234567890",
  "otp": "123456"
}
```

#### Get Profile
Retrieves the profile of the currently logged-in user.
- **Method**: `GET /user/profile`

#### Update Profile
Updates the profile of the currently logged-in user.
- **Method**: `POST /user/profile`
- **Body**: `Record` object with updated attributes.

#### Logout
Logs out the current user.
- **Method**: `POST /user/logout`

#### Delete Account
Deletes the current user's account.
- **Method**: `POST /user/delete`

#### Request OTP
Requests an OTP for login or verification.
- **Method**: `POST /user/otp-request`
- **Body**:
```json
{
  "email": "jdoe@example.com"
}
```

#### Request OTP for Login
Requests an OTP specifically for login purposes.
- **Method**: `POST /user/otp-request-login`
- **Body**:
```json
{
  "email": "jdoe@example.com"
}
```

#### Password Reset Request
Initiates the password reset process.
- **Method**: `POST /user/password-reset-request`
- **Body**:
```json
{
  "email": "jdoe@example.com"
}
```

#### Confirm OTP
Verifies the OTP sent to the user.
- **Method**: `POST /user/otp-confirm`
- **Body**:
```json
{
  "email": "jdoe@example.com",
  "code": "123456"
}
```

#### Reset User Password (Admin/Self)
Resets a user's password (requires appropriate permissions).
- **Method**: `POST /user/reset`
- **Body**:
```json
{
  "shortname": "jdoe"
}
```

#### Validate Password
Checks if the provided password is correct for the current user.
- **Method**: `POST /user/validate_password`
- **Body**: `password` (string)

#### Social Login Callbacks
Handles callbacks from social login providers.
- **Google**: `GET /user/google/callback`
- **Facebook**: `GET /user/facebook/callback`
- **Apple**: `GET /user/apple/callback`

---

### Managed Content (`/managed`)
Endpoints for authenticated management of content and resources.

#### Import Data
Imports data from a ZIP file.
- **Method**: `POST /managed/import`
- **Body**: `multipart/form-data` with `zip_file`.

#### Export Data
Exports data based on a query.
- **Method**: `POST /managed/export`
- **Body**: `Query` object.

#### Generate CSV from Query
Generates a CSV file from a saved query report.
- **Method**: `POST /managed/csv/{space_name}`
- **Body**: `Record` object representing the report.

#### Export CSV
Exports query results as CSV.
- **Method**: `POST /managed/csv`
- **Body**: `Query` object.

#### General Query
Executes a query against the database.
- **Method**: `POST /managed/query`
- **Body**: `Query` object.
- **Example**:
```json
{
  "type": "search",
  "space_name": "data",
  "subpath": "/content",
  "search": "*",
  "limit": 5
}
```

#### Submit Request
Performs batch operations (create, update, delete, etc.).
- **Method**: `POST /managed/request`
- **Body**: `Request` object.
- **Example (Create Content)**:
```json
{
  "space_name": "data",
  "request_type": "create",
  "records": [
    {
      "resource_type": "content",
      "shortname": "new-item",
      "subpath": "/items",
      "attributes": {
        "displayname": {"en": "New Item"},
        "payload": {
          "content_type": "json",
          "body": {"key": "value"}
        }
      }
    }
  ]
}
```

#### Progress Ticket
Updates the state of a ticket workflow.
- **Method**: `PUT /managed/progress-ticket/{space_name}/{subpath}/{shortname}/{action}`
- **Body**:
```json
{
  "resolution": "Fixed",
  "comment": "Done"
}
```

#### Retrieve Payload
Gets the raw payload of a resource.
- **Method**: `GET /managed/payload/{resource_type}/{space_name}/{subpath}/{shortname}.{ext}`

#### Create/Update Resource with Payload
Uploads a file as payload for a resource.
- **Method**: `POST /managed/resource_with_payload`
- **Body**: `multipart/form-data`
  - `payload_file`: The file to upload.
  - `request_record`: JSON string of the `Record`.
  - `space_name`: String.

#### Import Resources from CSV
Creates resources from a CSV file.
- **Method**: `POST /managed/resources_from_csv/{resource_type}/{space_name}/{subpath}/{schema_shortname}`
- **Body**: `multipart/form-data` with `resources_file`.

#### Retrieve Entry Metadata
Gets the metadata of a resource.
- **Method**: `GET /managed/entry/{resource_type}/{space_name}/{subpath}/{shortname}`

#### Get Entry by UUID
- **Method**: `GET /managed/byuuid/{uuid}`

#### Get Entry by Slug
- **Method**: `GET /managed/byslug/{slug}`

#### Health Check
Runs a health check on a space.
- **Method**: `GET /managed/health/{health_type}/{space_name}`
- **Types**: `soft`, `hard`

#### Lock/Unlock Entry
- **Lock**: `PUT /managed/lock/{resource_type}/{space_name}/{subpath}/{shortname}`
- **Unlock**: `DELETE /managed/lock/{space_name}/{subpath}/{shortname}`

#### Reload Security Data
Reloads permissions and roles (useful for file-based storage).
- **Method**: `GET /managed/reload-security-data`

#### Execute Task
Executes a specific task type (e.g., query) on a space.
- **Method**: `POST /managed/excute/{task_type}/{space_name}`

#### Apply Alteration
Applies a recorded alteration to an entry.
- **Method**: `POST /managed/apply-alteration/{space_name}/{alteration_name}`

#### Shortened URL Redirect
Redirects a short token to its original URL.
- **Method**: `GET /managed/s/{token}`

---

### Public Access (`/public`)
Endpoints for unauthenticated or public access (if configured).

#### Public Query
Executes a query publicly.
- **Method**: `POST /public/query`
- **Body**: `Query` object.

#### Public Query via URL Params
- **Method**: `GET /public/query/{type}/{space_name}/{subpath}`

#### Retrieve Entry
- **Method**: `GET /public/entry/{resource_type}/{space_name}/{subpath}/{shortname}`

#### Retrieve Payload
- **Method**: `GET /public/payload/{resource_type}/{space_name}/{subpath}/{shortname}.{ext}`

#### Public Submit
Submits data to a public endpoint (e.g., a form).
- **Method**: `POST /public/submit/{space_name}/{schema_shortname}/{subpath}`
- **Body**: JSON object matching the schema.

#### Attach File (Public)
Attaches a file to a record.
- **Method**: `POST /public/attach/{space_name}`

#### Execute Task (Public)
- **Method**: `POST /public/excute/{task_type}/{space_name}`

#### Get Entry by UUID (Public)
- **Method**: `GET /public/byuuid/{uuid}`

#### Get Entry by Slug (Public)
- **Method**: `GET /public/byslug/{slug}`

---

### QR Codes (`/qr`)

#### Generate QR Code
Generates a QR code for a resource.
- **Method**: `GET /qr/generate/{resource_type}/{space_name}/{subpath}/{shortname}`

#### Validate QR Code
Validates a scanned QR code.
- **Method**: `POST /qr/validate`
- **Body**:
```json
{
  "resource_type": "user",
  "space_name": "data",
  "subpath": "/users",
  "shortname": "jdoe",
  "qr_data": "<scanned_string>"
}
```

---

### System Info (`/info`)

#### Get Current User Info
- **Method**: `GET /info/me`

#### Get System Settings
(Restricted to 'dmart' user)
- **Method**: `GET /info/settings`

#### Get System Manifest
Returns system version and status.
- **Method**: `GET /info/manifest`
