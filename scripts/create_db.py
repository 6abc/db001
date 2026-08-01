#!/usr/bin/env python3

import subprocess
import sys
import getpass


def run_sql(sql):
    cmd = [
        "sudo",
        "-u",
        "postgres",
        "psql",
        "-v",
        "ON_ERROR_STOP=1",
    ]

    result = subprocess.run(
        cmd,
        input=sql,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        print("\n❌ PostgreSQL Error:")
        print(result.stderr)
        sys.exit(1)


def main():
    print("=" * 50)
    print(" PostgreSQL Database Creation Wizard")
    print("=" * 50)

    db_name = input("Database Name : ").strip()
    db_user = input("Database User : ").strip()
    db_pass = getpass.getpass("Database Password : ")

    if not db_name or not db_user or not db_pass:
        print("\n❌ All fields are required.")
        sys.exit(1)

    sql = f"""
    CREATE DATABASE "{db_name}";

    CREATE USER "{db_user}" WITH PASSWORD '{db_pass}';

    GRANT ALL PRIVILEGES ON DATABASE "{db_name}" TO "{db_user}";

    ALTER DATABASE "{db_name}" OWNER TO "{db_user}";

    \\connect "{db_name}"

    GRANT ALL ON SCHEMA public TO "{db_user}";
    ALTER SCHEMA public OWNER TO "{db_user}";
    """

    print("\nCreating database...")
    run_sql(sql)

    print("\n✅ Done!")
    print("-" * 50)
    print(f"Database : {db_name}")
    print(f"User     : {db_user}")
    print("Privileges: Granted")
    print("-" * 50)


if __name__ == "__main__":
    main()
