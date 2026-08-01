#!/usr/bin/env python3

import subprocess
import os
import datetime
import getpass
import sys

print("=" * 50)
print("PostgreSQL Backup Wizard")
print("=" * 50)

db_name = input("Database Name : ").strip()
db_user = input("Database User : ").strip()
db_pass = getpass.getpass("Database Password : ")

backup_dir = input("Backup Folder [backups]: ").strip() or "backups"

os.makedirs(backup_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(
    backup_dir,
    f"{db_name}_{timestamp}.sql"
)

env = os.environ.copy()
env["PGPASSWORD"] = db_pass

cmd = [
    "pg_dump",
    "-h",
    "localhost",
    "-U",
    db_user,
    "-F",
    "p",
    "-d",
    db_name,
    "-f",
    backup_file,
]

result = subprocess.run(cmd, env=env)

if result.returncode != 0:
    print("\n❌ Backup failed.")
    sys.exit(1)

print("\n✅ Backup completed.")
print(f"Saved to: {backup_file}")
