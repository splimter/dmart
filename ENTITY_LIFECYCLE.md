# Entity Lifecycle & Management

This document provides a technical overview of the entity lifecycle within the D-MART platform, catering to developers who need to understand how to create, manage, and interact with data entities programmatically or via the file system.

## Overview

In D-MART, almost everything is an **Entity** (or Resource). Entities are the fundamental units of data storage and management. They are defined by a common structure that includes metadata and a payload.

### Core Structure

Every entity consists of two main parts:

1.  **Meta**: Contains system-level metadata such as UUID, shortname, ownership, creation/update timestamps, and access control lists (ACLs).
2.  **Payload**: Contains the actual content or body of the entity, along with its type (e.g., JSON, Markdown, Image) and schema reference.

#### Meta Structure (JSON Representation)

```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "shortname": "unique_entity_id",
  "slug": "user-friendly-slug",
  "is_active": true,
  "displayname": {
    "en": "Entity Name",
    "ar": "اسم الكيان",
    "ku": "Navê Heyber"
  },
  "description": {
    "en": "Description here",
    "ar": "الوصف هنا"
  },
  "tags": ["tag1", "tag2"],
  "created_at": "2023-10-27T10:00:00",
  "updated_at": "2023-10-27T10:00:00",
  "owner_shortname": "admin_user",
  "owner_group_shortname": "editors",
  "payload": {
    "content_type": "json",
    "schema_shortname": "custom_schema",
    "body": {
      "key": "value"
    }
  }
}
```

## Creating and Managing Entities

Entities can be managed through the REST API or, in the default `file` adapter mode, directly via the file system.

### 1. Via REST API (`/managed/request`)

The primary endpoint for CRUD operations is `/managed/request`. It accepts a batch of records and an action type.

**Endpoint**: `POST /managed/request`

**Request Body Example (Create):**

```json
{
  "space_name": "data",
  "request_type": "create",
  "records": [
    {
      "resource_type": "content",
      "shortname": "my_new_article",
      "subpath": "/articles",
      "attributes": {
        "is_active": true,
        "displayname": { "en": "My New Article" },
        "payload": {
          "content_type": "markdown",
          "body": "# Hello World"
        }
      }
    }
  ]
}
```

**Supported Request Types:**
*   `create`: Create new entities.
*   `update`: Update existing entities (partial or full).
*   `delete`: Remove entities.
*   `move`: Move entities to a different space or subpath.
*   `assign`: Change ownership or group assignment.
*   `update_acl`: Modify Access Control Lists.
*   `patch`: Patch specific fields.

### 2. Via File System (File Adapter)

When D-MART is configured to use the `file` adapter (default), entities are stored as JSON files in the `spaces` directory.

**Directory Structure:**

```
spaces/
├── space_name/
│   ├── subpath/
│   │   ├── .dm/
│   │   │   ├── entity_shortname/
│   │   │   │   ├── meta.content.json  (The Meta object)
│   │   │   │   └── history/           (Version history)
│   │   └── entity_shortname.json      (The Payload body, if separated)
```

To "create" an entity manually:
1.  Create the directory structure.
2.  Add the `meta.<type>.json` file.
3.  (Optional) Add the payload file if the body is externalized.

## Types of Records

D-MART supports various `ResourceType`s, each serving a specific purpose. Common types include:

*   **Core**: `space`, `folder`, `user`, `group`, `role`, `permission`.
*   **Data**: `content`, `schema`, `json`, `file`, `media`.
*   **Social**: `post`, `comment`, `reaction`, `share`.
*   **Workflow**: `ticket`.
*   **System**: `log`, `notification`, `plugin_wrapper`, `history`.
*   **Big Data**: `parquet`, `csv`, `jsonl`, `sqlite`, `duckdb`.

## Special Entities in Management Space

The `management` space is a reserved space containing system-critical entities. These are typically stored in hidden `.dm/` directories to prevent accidental modification via standard content APIs.

### Users, Groups, Roles, Permissions

These security primitives are stored in specific subpaths within the `management` space:

*   **Users**: `management/users/.dm/<username>/meta.user.json`
*   **Groups**: `management/groups/.dm/<groupname>/meta.group.json`
*   **Roles**: `management/roles/.dm/<rolename>/meta.role.json`
*   **Permissions**: `management/permissions/.dm/<permname>/meta.permission.json`

### Management Entity Examples

#### Role (Meta)
Defines a collection of permissions.

```json
{
  "resource_type": "role",
  "shortname": "editor",
  "is_active": true,
  "permissions": ["read_all", "write_content"]
}
```

#### Permission (Meta)
Defines granular access controls (Actions, Conditions, Restrictions).

```json
{
  "resource_type": "permission",
  "shortname": "write_content",
  "subpaths": {
    "data": ["/articles", "/news"]
  },
  "resource_types": ["content", "media"],
  "actions": ["create", "update", "view"],
  "conditions": ["is_active", "own"],
  "restricted_fields": ["owner_shortname"],
  "allowed_fields_values": {}
}
```

#### Group (Meta)
Aggregates roles.

```json
{
  "resource_type": "group",
  "shortname": "editors_group",
  "roles": ["editor"]
}
```
