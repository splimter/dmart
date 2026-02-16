# Plugins

D-MART comes with a powerful plugin system that allows you to extend its functionality. Plugins can intercept events (hooks) or add new API endpoints.

## Pre-bundled Plugins

The following plugins are included with D-MART:

- **action_log**: Logs all creation, update, and deletion actions to a JSONL file for audit purposes.
- **admin_notification_sender**: Sends notifications to administrators when specific content is created (e.g., admin notification requests).
- **ldap_manager**: Synchronizes user creation and updates with an LDAP server (inactive by default).
- **local_notification**: Handles local notifications for tickets, reactions, and comments within the system.
- **realtime_updates_notifier**: Notifies connected clients of real-time updates (e.g., via WebSocket) when resources are modified.
- **redis_db_update**: Updates the Redis index when resources are created, updated, or deleted to ensure search results are up-to-date (inactive by default).
- **resource_folders_creation**: Automatically creates necessary folder structures when a new user or space is created.
- **system_notification_sender**: Sends system-wide notifications for various actions (inactive by default).
- **update_access_controls**: Updates access control lists (ACLs) when roles, groups, permissions, or users are modified.

## Defining Custom Plugins

You can extend D-MART by creating your own custom plugins.

### Location

Custom plugins must be placed in the `custom_plugins` directory within your spaces folder:
`spaces/custom_plugins/`

Each plugin should have its own directory containing two required files:
1. `config.json`
2. `plugin.py`

### Configuration (`config.json`)

The `config.json` file defines the plugin's metadata and behavior.

```json
{
  "shortname": "my_custom_plugin",
  "is_active": true,
  "type": "hook",
  "listen_time": "after",
  "ordinal": 10,
  "filters": {
    "subpaths": ["__ALL__"],
    "resource_types": ["content", "user"],
    "schema_shortnames": ["__ALL__"],
    "actions": ["create", "update"]
  }
}
```

*   **shortname**: A unique identifier for your plugin.
*   **is_active**: Set to `true` to enable the plugin.
*   **type**: define the type of the plugin, allowed values:
    *   `hook`: The plugin reacts to system events.
    *   `api`: The plugin adds new API endpoints.
*   **listen_time**: (For hooks) When the plugin should execute relative to the action.
    *   `before`: Execute before the action is committed (can block or modify).
    *   `after`: Execute after the action is committed (good for logging, notifications).
*   **ordinal**: Determines the execution order relative to other plugins (lower numbers run first).
*   **filters**: (For hooks) Defines which events trigger the plugin.
    *   `subpaths`: List of subpaths to listen on (or `__ALL__`).
    *   `resource_types`: List of resource types to listen for (e.g., `content`, `user`).
    *   `schema_shortnames`: Specific schemas to filter by (or `__ALL__`).
    *   `actions`: List of actions to listen for (e.g., `create`, `update`, `delete`).

### Implementation (`plugin.py`)

The `plugin.py` file contains the Python code for your plugin.

#### Hook Plugins

For `hook` plugins, you must define a `Plugin` class that inherits from `PluginBase` and implements the `hook` method.

```python
from models.core import PluginBase, Event

class Plugin(PluginBase):
    async def hook(self, data: Event):
        # Your custom logic here
        print(f"Event received: {data.action_type} on {data.resource_type}")
```

The `Event` object contains details about the action, such as `space_name`, `subpath`, `resource_type`, `action_type`, and `attributes`.

#### API Plugins

For `api` plugins, you must define a `router` object (typically an `APIRouter` from FastAPI). The system will automatically mount this router.

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
async def hello():
    return {"message": "Hello from my custom plugin!"}
```

The endpoints will be available under `/{plugin_shortname}/...`.
