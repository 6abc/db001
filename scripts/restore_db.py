#!/usr/bin/env python3

import os
import sys
import subprocess
import getpass


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
        print(result.stderr)
        sys.exit(result.returncode)


print("=" * 60)
print(" PostgreSQL Restore Wizard")
print("=" * 60)

# Backup file
while True:
    backup_file = input("\nBackup SQL File: ").strip()

    # Remove quotes if file is dragged into terminal
    backup_file = backup_file.strip('"').strip("'")

    if os.path.isfile(backup_file):
        break

    print("❌ File not found.")

print()

db_name = input("Database Name     : ").strip()
db_user = input("Database User     : ").strip()
db_pass = getpass.getpass("Database Password : ")

print("\nChecking PostgreSQL user...")

run_postgres(f"""
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT
        FROM pg_roles
        WHERE rolname = '{db_user}'
    ) THEN
        CREATE USER "{db_user}" WITH PASSWORD '{db_pass}';
    END IF;
END
$$;
""")

print("Checking database...")

run_postgres(f"""
SELECT 'CREATE DATABASE "{db_name}" OWNER "{db_user}"'
WHERE NOT EXISTS (
    SELECT
    FROM pg_database
    WHERE datname = '{db_name}'
)
\\gexec
""")

print("Setting ownership and permissions...")

run_postgres(f"""
ALTER DATABASE "{db_name}" OWNER TO "{db_user}";

\\connect "{db_name}"

GRANT ALL ON SCHEMA public TO "{db_user}";
ALTER SCHEMA public OWNER TO "{db_user}";
""")

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

print("\n" + "=" * 60)
print("✅ Restore completed successfully.")
print("=" * 60)
print(f"Database : {db_name}")
print(f"User     : {db_user}")
print(f"Backup   : {backup_file}")
print("=" * 60)
