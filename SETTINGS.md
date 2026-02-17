# Configuration Settings

This document details all the configurable settings available in D-MART. These settings are defined in `backend/utils/settings.py` and can be configured via environment variables, a `config.env` file, or a JSON configuration file.

## Introduction

Settings are loaded using `pydantic-settings`. The application looks for configuration in the following order:
1.  Environment variables.
2.  A file specified by the `BACKEND_ENV` environment variable.
3.  `config.env` in the current directory.
4.  `~/.dmart/config.env`.

## General Configuration

*   **`app_name`**: The name of the application. Default: `"dmart"`.
*   **`app_url`**: The base URL where the application is hosted. Default: `""`.
*   **`public_app_url`**: The publicly accessible URL of the application, used for external links. Default: `""`.
*   **`base_path`**: A URL path prefix for the application (e.g., `/api`). Default: `""`.
*   **`debug_enabled`**: Enables debug mode, which may expose more detailed error information. Default: `True`.
*   **`debug_perm`**: specialized debug flag, likely for permissions debugging. Default: `False`.
*   **`hide_stack_trace`**: If set to `True`, stack traces are hidden from error responses even if debug mode is on. Default: `False`.

## Server & Network

*   **`listening_host`**: The hostname or IP address the server binds to. Default: `"0.0.0.0"`.
*   **`listening_port`**: The port the server listens on. Default: `8282`.
*   **`request_timeout`**: The maximum time (in seconds) allowed for processing a request. Default: `35`.
*   **`websocket_url`**: The URL for WebSocket connections. Default: `""` (constructed dynamically if empty).
*   **`websocket_port`**: The port for WebSocket connections. Default: `8484`.
*   **`cors_origins`**: (Configured via `backend/main.py` logic, not directly in settings) Controls Access-Control-Allow-Origin headers.

## Database & Storage

D-MART supports two modes for data persistence (`active_data_db`) and two modes for operational data (`active_operational_db`).

*   **`active_data_db`**: The primary storage backend. Options:
    *   `"file"`: Uses the file system for storage and Redis for indexing (default).
    *   `"sql"`: Uses a SQL database for both storage and indexing.
*   **`active_operational_db`**: The operational database (e.g., for sessions, caching). Options:
    *   `"redis"` (default).
    *   `"manticore"`.

### SQL Database Settings
Used when `active_data_db` is set to `"sql"`.

*   **`database_driver`**: The SQLAlchemy driver to use. Default: `"sqlite+pysqlite"`.
*   **`database_host`**: Database hostname. Default: `"localhost"`.
*   **`database_port`**: Database port. Default: `5432`.
*   **`database_username`**: Database username. Default: `"postgres"`.
*   **`database_password`**: Database password. Default: `""`.
*   **`database_name`**: Database name. Default: `"dmart"`.
*   **`database_pool_size`**: Connection pool size. Default: `2`.
*   **`database_max_overflow`**: Max overflow connections. Default: `2`.
*   **`database_pool_timeout`**: Pool timeout in seconds. Default: `30`.
*   **`database_pool_recycle`**: Pool recycle time in seconds. Default: `30`.

### Redis Settings
Used for operational data and indexing when `active_data_db` is `"file"`.

*   **`redis_host`**: Redis hostname. Default: `"127.0.0.1"`.
*   **`redis_port`**: Redis port. Default: `6379`.
*   **`redis_password`**: Redis password. Default: `""`.
*   **`redis_pool_max_connections`**: Max connections in the Redis pool. Default: `20`.

### File System Settings
*   **`files_query`**: Method used for querying files. Default: `"scandir"`.

## Security & Authentication

*   **`jwt_secret`**: Secret key used for signing JWT tokens. **Crucial:** Change this in production. Default: Randomly generated string.
*   **`jwt_algorithm`**: Algorithm used for JWT. Default: `"HS256"`.
*   **`jwt_access_expires`**: JWT expiration time in seconds. Default: `2592000` (30 days).
*   **`max_sessions_per_user`**: Maximum number of concurrent sessions allowed per user. Default: `5`.
*   **`session_inactivity_ttl`**: Time (in seconds) before an inactive session expires. `0` disables this feature. Default: `0`.
*   **`max_failed_login_attempts`**: Number of failed login attempts before lockout/throttling. Default: `5`.
*   **`lock_period`**: Duration (in seconds) for account lockout or resource locking. Default: `300`.
*   **`is_registrable`**: Allows new users to register themselves. Default: `True`.
*   **`social_login_allowed`**: Enables social login options. Default: `True`.
*   **`is_otp_for_create_required`**: Requires OTP verification for account creation. Default: `True`.
*   **`otp_token_ttl`**: Time-to-live for OTP tokens in seconds. Default: `300` (5 minutes).
*   **`allow_otp_resend_after`**: Time (in seconds) before a new OTP can be requested. Default: `60`.
*   **`user_profile_payload_protected_fields`**: List of fields in the user profile that users cannot update themselves. Default: `[]`.
*   **`logout_on_pwd_change`**: Forces logout of all sessions when a user changes their password. Default: `True`.

## Email & Notifications

### SMTP Configuration
*   **`mail_driver`**: Mail driver to use. Default: `"smtp"`.
*   **`mail_host`**: SMTP server host. Default: `""`.
*   **`mail_port`**: SMTP server port. Default: `587`.
*   **`mail_username`**: SMTP username. Default: `""`.
*   **`mail_password`**: SMTP password. Default: `""`.
*   **`mail_encryption`**: Encryption method (`tls` or `ssl`). Default: `"tls"`.
*   **`mail_from_address`**: Email address for outgoing mails. Default: `"noreply@admin.com"`.
*   **`mail_from_name`**: Name for outgoing mails. Default: `""`.
*   **`mock_smtp_api`**: If `True`, mocks SMTP calls (useful for dev/test). Default: `True`.

### SMS & SMPP Configuration
*   **`send_sms_api`**: API endpoint for sending SMS. Default: `""`.
*   **`send_sms_otp_api`**: API endpoint specifically for OTP SMS. Default: `""`.
*   **`sms_sender`**: Sender ID for SMS. Default: `""`.
*   **`smpp_auth_key`**: Authentication key for SMPP. Default: `""`.
*   **`mock_smpp_api`**: Mocks SMPP calls. Default: `True`.
*   **`comms_api`**: General communications API endpoint. Default: `""`.

## Paths & Directories

*   **`spaces_folder`**: Directory path where spaces and their data are stored. Default: `../sample/spaces/`.
*   **`management_space`**: Name of the management space. Default: `"management"`.
*   **`users_subpath`**: Subpath where user data is stored within the management space. Default: `"users"`.
*   **`cxb_url`**: URL path for the frontend (CXB). Default: `"/cxb"`.
*   **`cxb_config_path`**: Path to the CXB configuration file. Default: `""` (auto-discovered).
*   **`log_file`**: Path to the application log file. Default: `"../logs/dmart.ljson.log"`.
*   **`ws_log_file`**: Path to the WebSocket log file. Default: `"../logs/websocket.ljson.log"`.

## Third-Party Integrations

### OAuth Providers
*   **`google_client_id`**, **`google_client_secret`**: Google OAuth credentials.
*   **`apple_client_id`**, **`apple_client_secret`**: Apple OAuth credentials.
*   **`facebook_client_id`**, **`facebook_client_secret`**: Facebook OAuth credentials.
*   **`google_application_credentials`**: Path to Google Application Credentials JSON file.

### LDAP
*   **`ldap_url`**: LDAP server URL. Default: `"ldap://"`.
*   **`ldap_admin_dn`**: LDAP Admin DN. Default: `""`.
*   **`ldap_root_dn`**: LDAP Root DN. Default: `""`.
*   **`ldap_pass`**: LDAP Password. Default: `""`.

## Miscellaneous

*   **`auto_uuid_rule`**: Rule for UUID generation. Default: `"auto"`.
*   **`jq_timeout`**: Timeout for JQ processing in seconds. Default: `2`.
*   **`url_shorter_expires`**: Expiration time for shortened URLs in seconds. Default: `172800` (48 hours).
*   **`is_sha_required`**: If `True`, enables optimistic locking/conflict detection by requiring the `last_checksum_history` attribute in update requests. Default: `False`.
*   **`mock_otp_code`**: Fixed OTP code for testing/mocking. Default: `"123456"`.
*   **`invitation_link`**: Base URL for invitation links. Default: `""`.
*   **`store_payload_string`**: Controls how payloads are stored. Default: `True`.
*   **`enable_channel_auth`**: Enables channel-based authentication. Default: `False`.
*   **`channels`**: Configuration for channels (loaded from `config/channels.json` if present).
*   **`allowed_submit_models`**: Dictionary of allowed models for submission (parsed from `allowed_submit_models` string).
*   **`max_query_limit`**: Hard limit on the number of results returned by a query. Default: `10000`.
