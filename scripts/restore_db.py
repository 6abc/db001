#!/usr/bin/env python3

import os
import sys
import subprocess
import getpass

BACKUP_DIR = "backups"


def run(cmd, env=None):
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        sys.exit(result.returncode)


def run_postgres(sql):
    result = subprocess.run(
        [
            "sudo",
            "-u",
            "postgres",
            "psql",
            "-v",
            "ON_ERROR_STOP=1",
        ],
        input=sql,
        text=True,
    )

    if result.returncode != 0:
        sys.exit(result.returncode)


print("=" * 50)
print("PostgreSQL Restore Wizard")
print("=" * 50)

if not os.path.isdir(BACKUP_DIR):
    print(f"Backup folder '{BACKUP_DIR}' does not exist.")
    sys.exit(1)

files = sorted(
    f for f in os.listdir(BACKUP_DIR)
    if f.endswith(".sql")
)

if not files:
    print("No SQL backup files found.")
    sys.exit(1)

print("\nAvailable Backups\n")

for i, file in enumerate(files, start=1):
    size = os.path.getsize(os.path.join(BACKUP_DIR, file))
    print(f"{i}. {file} ({size/1024/1024:.2f} MB)")

while True:
    try:
        choice = int(input("\nSelect backup number: "))
        if 1 <= choice <= len(files):
            break
    except ValueError:
        pass

    print("Invalid selection.")

backup_file = os.path.join(BACKUP_DIR, files[choice - 1])

print()

db_name = input("Database Name : ").strip()
db_user = input("Database User : ").strip()
db_pass = getpass.getpass("Database Password : ")

print("\nChecking database...")

sql = f"""
SELECT 'CREATE DATABASE "{db_name}"'
WHERE NOT EXISTS (
    SELECT FROM pg_database
    WHERE datname = '{db_name}'
)
\\gexec

ALTER DATABASE "{db_name}" OWNER TO "{db_user}";
"""

run_postgres(sql)

print("Restoring backup...")

env = os.environ.copy()
env["PGPASSWORD"] = db_pass

run(
    [
        "psql",
        "-h",
        "localhost",
        "-U",
        db_user,
        "-d",
        db_name,
        "-f",
        backup_file,
    ],
    env=env,
)

print("\n" + "=" * 50)
print("✅ Restore completed successfully.")
print("=" * 50)
print(f"Database : {db_name}")
print(f"Backup   : {os.path.basename(backup_file)}")
print("=" * 50)
