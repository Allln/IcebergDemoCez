import argparse
import trino
import time
import sys

SCHEMA = "test_db"
TABLE = "api_users"
def connect():
    for _ in range(10):
        try:
            conn = trino.dbapi.connect(
                host="trino",
                port=8080,
                user="admin",
                catalog="iceberg",
                schema=SCHEMA,
                http_scheme="http"
            )
            cur = conn.cursor()
            cur.execute("SELECT 1")
            return conn
        except:
            time.sleep(2)
    raise Exception("--- Could not connect to Trino ---")

def ensure_table():
    cur = connect().cursor()
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS iceberg.{SCHEMA}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS iceberg.{SCHEMA}.{TABLE} (
            id INT,
            name VARCHAR,
            created_at TIMESTAMP
        )
    """)

def create_table():
    ensure_table()
    print("--- Table created (or already existed) ---")

def insert_record(id, name):
    ensure_table()
    cur = connect().cursor()
    safe_name = name.replace("'", "''")
    cur.execute(f"""
        INSERT INTO iceberg.{SCHEMA}.{TABLE}
        VALUES ({int(id)}, '{safe_name}', current_timestamp)
    """)
    print("--- Inserted ---")

def select_records():
    ensure_table()
    cur = connect().cursor()
    cur.execute(f"SELECT * FROM iceberg.{SCHEMA}.{TABLE}")
    for row in cur.fetchall():
        print(row)

def delete_record(id):
    ensure_table()
    cur = connect().cursor()
    cur.execute(f"""
        DELETE FROM iceberg.{SCHEMA}.{TABLE}
        WHERE id = {int(id)}
    """)
    print("--- Deleted ---")

def update_record(id, name):
    ensure_table()
    cur = connect().cursor()
    safe_name = name.replace("'", "''")
    cur.execute(f"""
        UPDATE iceberg.{SCHEMA}.{TABLE}
        SET name = '{safe_name}'
        WHERE id = {int(id)}
    """)
    print("--- Updated ---")

def main():
    parser = argparse.ArgumentParser(description="Iceberg-Trino CLI")
    parser.add_argument("command", choices=["create_table", "insert", "select", "delete", "update"], help="Operation to perform")
    parser.add_argument("args", nargs="*", help="Arguments for the operationss")
    args = parser.parse_args()
    try:
        if args.command == "create_table":
            create_table()

        elif args.command == "insert":
            if len(args.args) != 2:
                raise ValueError("Usage: insert <id> <name>")
            insert_record(int(args.args[0]), args.args[1])
        elif args.command == "select":
            if len(args.args) != 0:
                raise ValueError("Usage: select")
            select_records()
        elif args.command == "delete":
            if len(args.args) != 1:
                raise ValueError("Usage: delete <id>")
            delete_record(int(args.args[0]))
        elif args.command == "update":
            if len(args.args) != 2:
                raise ValueError("Usage: update <id> <name>")
            update_record(int(args.args[0]), args.args[1])

    except ValueError as ve:
        print("--- FAIL ---", ve)
        parser.print_help()
        sys.exit(1)

    except Exception as e:
        print("--- Unexpected error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
