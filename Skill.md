# D-MART Core Skills for AI Agents

As an autonomous AI agent working within or interfacing with the D-MART ecosystem, your primary objective is to reliably implement, extend, and consume features built upon D-MART.

This document outlines the core domain knowledge ("skills") you need to interact safely and effectively with D-MART.

---

## 1. D-MART's Core Philosophy

D-MART is a **Data-as-a-Service (DaaS)** platform strictly adhering to a **Data-First** philosophy. Its primary goal is not to be a massive big-data lake (it is optimized for <=300M primary entries) but a highly structured, hierarchical information management system.

*   **Entries, Not Rows:** The fundamental atomic unit is the **entry**. An entry encapsulates all meta-information, a structured JSON payload, and arbitrary attachments (e.g., media, relations) into a single cohesive entity.
*   **Spaces and Subpaths:** Entries live within logical business domains called **spaces** and are organized hierarchically via **subpaths** (e.g., `/content/users/active`).
*   **Unique Identifiers:** Each entry is uniquely identified by its `shortname` within a given `subpath`.
*   **Hidden Meta Structures:** D-MART stores meta information and attachments in hidden `.dm` folders (e.g., `.dm/meta.user.json`, `.dm/attachments.media/`).

## 2. Persistence & Storage Modality

D-MART abstracts data storage but supports two distinct persistence modes configured via the `active_data_db` setting. You must respect the current configuration:

1.  **File System (`'file'`):** Data is stored directly as open, flat JSON files on disk. Redis acts strictly as a high-speed search and retrieval index. This prevents vendor lock-in.
2.  **SQL Database (`'sql'`):** A standard SQL database (like PostgreSQL) handles both primary storage and indexing. When generating direct SQL queries, you must rigorously validate and quote dynamic table/column names to prevent SQL injection.

## 3. Communication & Protocols

You must interface with D-MART primarily through its standardized REST-like JSON API.

*   **Payload Constraints:** The D-MART API explicitly expects `Content-Type: application/json` for write operations.
*   **Data Models:** All API requests and responses strictly adhere to the Python Pydantic models defined in `backend/models/api.py` (e.g., `api.Request`, `api.Query`, `api.Response`) and `backend/models/core.py`.
*   **Optimistic Locking (Concurrency Control):** If the `is_sha_required` setting is enabled, you MUST calculate and provide the current document checksum history when issuing updates. If an update fails with a `409 Conflict`, you must refetch the document, reapply your logic, and retry.

## 4. Security & Access Control

D-MART enforces robust Access Control Lists (ACLs) and Role-Based Access Control (RBAC).

*   **Permissions Definition:** Roles and permissions are loaded from `.dm` subdirectories (e.g., `roles/.dm/`, `permissions/.dm/`) within management spaces.
*   **Resource Type Validation:** When interacting with the access control system (`backend/utils/access_control.py`), the `resource_type` parameter is strictly validated against the `ResourceType` enum (e.g., `user`, `content`, `ticket`, `schema`).
*   **Protected Fields:** Do not attempt to modify fields defined in `user_profile_payload_protected_fields`. These fields are strictly protected at the API level, overriding any role-based permissions.
*   **Subpath Enclosures:** Permissions are explicitly tied to subpaths, actions (e.g., `create`, `update`, `delete`, `view`), and conditions.

## 5. Security Posture & Vulnerability Mitigation

When writing Python backend code or integration scripts, adhere to these strict security policies:

*   **Jinja2 Escaping:** When generating emails or HTML (e.g., using `Environment`), `autoescape=True` MUST be enabled to prevent Cross-Site Scripting (XSS).
*   **Command Injection (`jq`):** D-MART utilizes `jq` via `subprocess.run` for complex querying. You MUST separate `jq` arguments strictly with `--` to eliminate command injection vectors.
*   **Timeout Enforcement:** Any external network calls using the `requests` library MUST include an explicit timeout (e.g., `timeout=10` or `timeout=30`) to mitigate Denial of Service (DoS).
*   **Insecure Temporary Files:** Never use hardcoded `/tmp` paths in tests or scripts. Utilize Python's `tempfile` module (e.g., `tempfile.TemporaryDirectory()`).
*   **Legacy Hashes:** Do NOT change legacy hash algorithms (e.g., SHA1, MD5) in the codebase. Doing so breaks existing data integrity and checksum calculations.
*   **CORS:** Cross-Origin Resource Sharing is strictly enforced. It defaults to safe local ports and blocks unauthorized origins.
*   **Dependency Management:** The user strictly prefers security audits focused on application code logic rather than scanning or upgrading dependency packages in requirements files.

## 6. Technical Stack Optimization

*   **GZip Middleware:** D-MART utilizes FastAPI `GZipMiddleware` with a minimum size of 1000 bytes. Ensure clients properly support `Accept-Encoding: gzip`.
*   **Middleware Parsing:** The `middle` middleware is highly optimized. It conditionally parses response bodies only if the `Content-Type` is JSON/text and the body size is under 100KB.
*   **Asynchronous Event Loop:** D-MART leverages `Hypercorn` and conditionally imports `uvloop` for enhanced performance.
*   **Testing Context:** The backend uses an older version of `pytest-asyncio` (1.3.0). Tests should utilize the `@pytest.mark.anyio` decorator instead of `asyncio_default_fixture_loop_scope`. Redis integration tests strictly require a live Redis instance with RediSearch capabilities; `fakeredis` is insufficient.

## 7. Extending D-MART (Plugins)

D-MART is extensible via a plugin system managed by `backend/utils/plugin_manager.py`.

*   **Core Plugins:** Located in `backend/plugins/` (e.g., `action_log`, `ldap_manager`, `redis_db_update`, `update_access_controls`).
*   **Custom Plugins:** Located in `custom_plugins/` within the spaces folder. Each plugin requires a `config.json` and a `plugin.py`.

## 8. Development Workflows

*   **Diagrams:** When generating or modifying project documentation in Markdown, utilize Mermaid diagrams. **Crucial:** You MUST quote node labels containing parentheses (e.g., `["Label (Text)"]`) to prevent parsing errors.
*   **Sync Protocols:** Preserve `http://` and `ws://` protocols for local sync processes (e.g., `backend/sync.py`). Do not attempt to automatically upgrade them to their secure equivalents.
