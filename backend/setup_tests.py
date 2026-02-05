import json
import os
from pathlib import Path
from utils.password_hashing import hash_password

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
SPACES_DIR = BASE_DIR.parent / "sample" / "spaces"
MANAGEMENT_DIR = SPACES_DIR / "management" / "users" / ".dm"

USERS = ["dmart", "alibaba"]
PASSWORD = "Password123!"

# Hash password
hashed_pw = hash_password(PASSWORD)
print(f"Hashed password generated.")

# Update user files
for user in USERS:
    user_file = MANAGEMENT_DIR / user / "meta.user.json"
    if user_file.exists():
        with open(user_file, "r") as f:
            data = json.load(f)

        data["password"] = hashed_pw
        data["is_active"] = True # Ensure user is active

        with open(user_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Updated {user} password.")
    else:
        print(f"Warning: {user_file} not found.")

# Create login_creds.sh
creds_path = BASE_DIR / "login_creds.sh"
creds_content = f"""#!/bin/bash

# Super manager login creds. Do not leave spaces in the value
export SUPERMAN='{{"shortname":"dmart","password":"{PASSWORD}"}}'

# Exctra account used for testing
export ALIBABA='{{"shortname":"alibaba","password":"{PASSWORD}"}}'
"""

with open(creds_path, "w") as f:
    f.write(creds_content)

print(f"Created {creds_path}")
