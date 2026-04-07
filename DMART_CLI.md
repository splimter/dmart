# DMART CLI Documentation

The `dmart.py` script is the primary entry point for managing the DMART backend. It provides a variety of commands for running the server, interacting via a CLI, managing data, performing migrations, and more.

## Usage

```bash
python backend/dmart.py <command> [arguments]
```

## Available Commands

### 1. `serve`
Starts the DMART FastAPI backend server using Hypercorn.

**Options:**
- `--open-cxb`: Opens the CXB (Client Experience Builder) page in the default web browser after the server starts.
- `--dmart-config <path>`: Specifies a custom path to the `config.env` file. Overrides the `BACKEND_ENV` environment variable.
- `--cxb-config <path>`: Specifies a custom path to the `config.json` file for CXB. Overrides the `DMART_CXB_CONFIG` environment variable.

**Example:**
```bash
python backend/dmart.py serve --open-cxb --dmart-config my_custom_config.env
```

### 2. `hyper`
Starts the application using Hypercorn with full access to Hypercorn's command-line arguments. This is useful for advanced server configuration.

**Arguments:**
- Accepts all standard `hypercorn` arguments (e.g., `-b`, `--bind`, `-w`, `--workers`, `--certfile`, `--keyfile`).
- `--open-cxb`: Opens the CXB page in the browser after starting.
- `--cxb-config <path>`: Path to CXB `config.json`.
- `--dmart-config <path>`: Path to dmart `config.env`.

**Example:**
```bash
python backend/dmart.py hyper -b 0.0.0.0:8000 -w 4
```

### 3. `cli`
Starts the interactive interactive shell/CLI for communicating with the DMART backend. It supports REPL, command execution, and running scripts.

**Options:**
- `--config <path>`: Path to the CLI configuration file (usually `cli.ini`).

**Example:**
```bash
python backend/dmart.py cli
python backend/dmart.py cli --config my_cli_config.ini
```

### 4. `ws`
Starts the standalone WebSocket server.

**Options:**
- `--dmart-config <path>`: Path to the dmart `config.env` file.

**Example:**
```bash
python backend/dmart.py ws --dmart-config prod_config.env
```

### 5. `wt`
Starts the standalone WebTransporter server.

**Options:**
- `--dmart-config <path>`: Path to the dmart `config.env` file.

**Example:**
```bash
python backend/dmart.py wt
```

### 6. `export`
Exports data from the database into a JSON-based file structure within a ZIP archive.

**Options:**
- `--space_name SPACE_NAME`: (Optional) The specific space to export. If not provided, all spaces are exported.
- `--output OUTPUT`: (Required) The path for the output ZIP file. If `.` is provided, it defaults to `<space_name>.zip` or `all_spaces.zip`.

**Example:**
```bash
python backend/dmart.py export --space_name management --output management_backup.zip
```

### 7. `import`
Imports data from a ZIP archive or a directory into the database.

**Arguments:**
- `target`: (Optional) The path to the ZIP file or directory to import. Defaults to the current directory (`.`).

**Example:**
```bash
python backend/dmart.py import my_backup.zip
```

### 8. `settings`
Prints the current application settings as a formatted JSON string.

**Example:**
```bash
python backend/dmart.py settings
```

### 9. `set_password`
Invokes the `set_admin_passwd` script to securely set or update an administrator password.

**Example:**
```bash
python backend/dmart.py set_password
```

### 10. `json_to_db`
Manually triggers the migration process to load data from the file-based JSON storage into the SQL database.

**Example:**
```bash
python backend/dmart.py json_to_db
```

### 11. `db_to_json`
Manually triggers the migration process to export data from the SQL database back to the file-based JSON storage structure.

**Example:**
```bash
python backend/dmart.py db_to_json
```

### 12. `update_query_policies`
Runs a script to update query policies in the SQL database.

**Example:**
```bash
python backend/dmart.py update_query_policies
```

### 13. `init`
Initializes the DMART environment by copying sample spaces to the `~/.dmart/spaces` directory. Overwrites the existing directory if it exists.

**Example:**
```bash
python backend/dmart.py init
```

### 14. `migrate`
Executes Alembic database migrations. By default, it runs `alembic upgrade head`.

**Arguments:**
- Accepts all standard `alembic` command-line arguments.

**Example:**
```bash
python backend/dmart.py migrate
python backend/dmart.py migrate revision --autogenerate -m "Add new table"
```

### 15. `test`
Sets up the environment for testing. Copies necessary shell scripts (`curl.pypi.sh` to `curl.sh`) and sample test data to the `~/.dmart` directory, then executes the script.

**Example:**
```bash
python backend/dmart.py test
```

### 16. `apply_plugin_config`
Reads `~/.dmart/plugins_config.json` and patches the configurations (`config.json`) of the respective plugins located in `backend/plugins`.

**Example:**
```bash
python backend/dmart.py apply_plugin_config
```

### 17. `info`
Prints detailed version information as formatted JSON, including the commit hash, date, branch, and tag.

**Example:**
```bash
python backend/dmart.py info
```

### 18. `version`
Prints the current Git tag of the application.

**Example:**
```bash
python backend/dmart.py version
```

### 19. `help`
Prints the list of available commands.

**Example:**
```bash
python backend/dmart.py help
```
