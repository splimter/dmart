# Agent Documentation (AGENTS.md)

Welcome, AI Agent. This document provides a detailed technical overview of how to interact with the D-MART ecosystem. D-MART is a Data-as-a-Service (DaaS) layer that abstracts and manages structured, unstructured, and binary data.

Your goal is to autonomously implement features based on D-MART by interacting with its standardized REST-like JSON API.

## 1. High-Level Interaction Model

You will interact with D-MART primarily through HTTP requests. The backend is built with FastAPI and strictly validates all requests and responses using Pydantic models.

**Key Technical Constraints:**

*   **API Payloads:** All write operations (Create, Update, Patch, Delete) generally require a JSON payload matching the `api.Request` model.
*   **Response Bodies:** The backend middleware is highly optimized. It only parses response bodies if the `Content-Type` is explicitly `application/json` or text, and the payload is under 100KB. Ensure your HTTP clients handle responses correctly, especially errors.
*   **GZip Compression:** The backend uses `GZipMiddleware` for responses > 1000 bytes. Your client must support `Accept-Encoding: gzip`.
*   **Security Context (JWT):** Most operations require authentication via a JWT Bearer token obtained from the `/user/login` endpoint.
*   **Optimistic Locking:** If `is_sha_required` is enabled, you must handle 409 Conflicts by fetching the latest document state, applying your changes, and retrying.

## 2. Core Concepts & Terminology

Before constructing API requests, you must understand the D-MART data model:

*   **Space (`space_name`):** The top-level business domain or tenant (e.g., `acme`, `internal`).
*   **Subpath (`subpath`):** A hierarchical logical path within a space (e.g., `users/active`, `products/electronics`). Must match regex pattern `regex.SUBPATH`.
*   **Shortname (`shortname`):** A unique identifier for an entry within its specific subpath (e.g., `johndoe`, `iphone-14`). Must match regex pattern `regex.SHORTNAME`.
*   **Resource Type (`resource_type`):** Defines the nature of the entry (e.g., `content`, `user`, `schema`, `ticket`). Found in `backend/models/enums.py`.
*   **Payload (`payload`):** The actual structured data (JSON) or binary content attached to an entry. Structured payloads require a corresponding `schema_shortname`.

## 3. Core API Interactions

Below is a detailed summary of the primary D-MART APIs, including their typical input structures and expected outputs. All routes are prefixed with the respective router path (e.g., `/user`, `/managed`, `/public`).

### A. Authentication & User Management (`/user` router)

#### 1. Login (`POST /user/login`)
Authenticates a user and returns a session payload including the JWT token.

*   **Input:** `UserLoginRequest` (JSON)
    ```json
    {
      "identifier": {"email": "user@example.com"}, // or msisdn, shortname
      "password": "securepassword",
      "user_type": "web"
    }
    ```
*   **Output:** `api.Response`
    ```json
    {
      "status": "success",
      "attributes": {
        "access_token": "eyJhbGciOiJIUzI...",
        "user_shortname": "johndoe"
      }
    }
    ```

#### 2. Create User (`POST /user/create`)
Provisions a new user account.

*   **Input:** `core.Record` (JSON)
    ```json
    {
      "resource_type": "user",
      "shortname": "newuser",
      "subpath": "users",
      "attributes": {
        "email": "newuser@example.com",
        "password": "securepassword123",
        "displayname": {"en": "New User"}
      }
    }
    ```
*   **Output:** `api.Response` (Success status and the created user record).

### B. Managed Data Operations (`/managed` router)

This router handles the bulk of CRUD operations for authenticated users.

#### 1. Query Entries (`POST /managed/query`)
The primary endpoint for retrieving and searching data. Supports RediSearch syntax.

*   **Input:** `api.Query` (JSON)
    ```json
    {
      "type": "search",
      "space_name": "acme",
      "subpath": "products",
      "filter_types": ["content"],
      "search": "@category:electronics @price:[100 500]",
      "limit": 10,
      "offset": 0,
      "retrieve_json_payload": true
    }
    ```
*   **Output:** `api.Response` containing a list of `core.Record` objects in `records`.

#### 2. Serve Request (CRUD Operations) (`POST /managed/request`)
Executes Create, Update, Patch, Delete, or Move operations on entries.

*   **Input:** `api.Request` (JSON)
    ```json
    {
      "space_name": "acme",
      "request_type": "create", // or update, delete, patch, move
      "records": [
        {
          "resource_type": "content",
          "shortname": "iphone-14",
          "subpath": "products",
          "attributes": {
            "displayname": {"en": "iPhone 14"},
            "payload": {
              "content_type": "json",
              "schema_shortname": "product_schema",
              "body": {
                "price": 799,
                "color": "black"
              }
            }
          }
        }
      ]
    }
    ```
*   **Output:** `api.Response` (Success status indicating the operation completed).

#### 3. Retrieve Entry Meta (`GET /managed/entry/{resource_type}/{space_name}/{subpath:path}/{shortname}`)
Fetches the metadata for a specific entry.

*   **Output:** `api.Response` containing the `core.Record`.

#### 4. Retrieve Payload (`GET /managed/payload/{resource_type}/{space_name}/{subpath:path}/{shortname}.{ext}`)
Downloads the actual payload file (JSON, binary, etc.) associated with an entry.

*   **Output:** The raw file content (e.g., `application/json` or `image/jpeg`).

#### 5. Update State (Workflows) (`PUT /managed/progress-ticket/{space_name}/{subpath:path}/{shortname}/{action}`)
Transitions a ticket/workflow entry to a new state.

*   **Output:** `api.Response` indicating success or failure based on workflow rules defined in the schema.

## 4. Security & Implementation Guidelines for AI Agents

When interacting with or extending D-MART, you MUST adhere to the following strict technical guidelines derived from the project's memory and architecture:

1.  **SQL Injection Prevention:** When working with the SQL Data Adapter (`active_data_db="sql"`), dynamic table names or column references used in raw SQLAlchemy text queries MUST be explicitly validated (e.g., ensuring they are alphanumeric) and safely quoted to prevent SQL injection vulnerabilities.
2.  **Command Injection Mitigation (`jq`):** D-MART utilizes the `jq` CLI utility via `subprocess.run` for complex query filtering. To prevent command injection, you MUST ensure that `jq` arguments are strictly separated by `--` in the subprocess call.
3.  **Cross-Site Scripting (XSS) Prevention:** When generating HTML or text-based emails, Jinja2 `Environment` instances MUST be initialized with `autoescape=True` enabled.
4.  **Denial of Service (DoS) Prevention:** All external network calls utilizing the `requests` library MUST include explicit timeouts (e.g., `timeout=10` or `timeout=30`).
5.  **Insecure Temporary Files:** Never use hardcoded paths like `/tmp` for temporary files or directories (e.g., during testing or plugin execution). Always use the Python `tempfile` module (e.g., `tempfile.TemporaryDirectory()`).
6.  **Protected Profile Fields:** Be aware that the `user_profile_payload_protected_fields` setting in `backend/utils/settings.py` prevents users (and agents acting on their behalf) from modifying specific fields in their own profile payload, regardless of their role permissions.
7.  **Legacy Integrity:** Do NOT change legacy hash algorithms (e.g., `SHA1`, `MD5`) in the codebase. Doing so will silently break existing data and checksum calculations.
8.  **Testing Constraints:**
    *   Integration tests require a live Redis instance with RediSearch capabilities; `fakeredis` is not sufficient.
    *   Use `@pytest.mark.anyio` for asynchronous tests, as the environment uses an older version of `pytest-asyncio` incompatible with newer default loop scopes.
    *   When testing API routes, explicitly remove the catch-all route (`/{x:path}`) defined in `backend/main.py` from `app.router.routes` to prevent it from shadowing dynamically defined test routes.
9.  **Markdown/Mermaid Syntax:** When modifying documentation, Mermaid diagrams require quoting for node labels containing parentheses (e.g., `["Label (Text)"]`) to prevent parsing errors.
10. **Sync Protocols:** Do NOT attempt to automatically upgrade `http://` or `ws://` protocols to secure equivalents (`https://`, `wss://`) for local sync processes defined in `backend/sync.py`.

By strictly adhering to these constraints and utilizing the API documentation above, you can safely and effectively build features within the D-MART ecosystem.
