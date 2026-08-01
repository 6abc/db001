#!/usr/bin/env python3

import subprocess
import sys


def run_sql(sql):
    result = subprocess.run(
        ["sudo", "-u", "postgres", "psql", "-v", "ON_ERROR_STOP=1"],
        input=sql,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("\n❌ Error:")
        print(result.stderr)
        sys.exit(1)


print("=" * 50)
print("PostgreSQL Database Deletion Wizard")
print("=" * 50)

db_name = input("Database Name : ").strip()
db_user = input("Database User : ").strip()

confirm = input(
    f"\n⚠️  Delete database '{db_name}' and user '{db_user}'? (yes/no): "
).lower()

if confirm != "yes":
    print("Cancelled.")
    sys.exit(0)

sql = f"""
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = '{db_name}'
AND pid <> pg_backend_pid();

DROP DATABASE IF EXISTS "{db_name}";
DROP USER IF EXISTS "{db_user}";
"""

print("\nDeleting...")
run_sql(sql)

print("\n✅ Database and user deleted successfully.")
