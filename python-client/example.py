import trino
from trino.auth import BasicAuthentication
import time

#helpers
def wait_for_trino(max_attempts=10, delay=5):
    for attempt in range(max_attempts):
        try:
            conn = trino.dbapi.connect(
                host='trino',
                port=8080,
                user='admin',
                catalog='iceberg',
                schema='test_db',
                http_scheme='http',
            )
            cur = conn.cursor()
            cur.execute("SELECT 1")
            print("--- Trino is ready ---")
            return conn
        except Exception as e:
            print(f"W8ing for Trino to be ready (attempt {attempt + 1})...")
            time.sleep(delay)
    raise RuntimeError("--- Trino did not become ready in time ---")

conn = wait_for_trino()

cur = conn.cursor()
cur.execute("CREATE SCHEMA IF NOT EXISTS iceberg.test_db")

cur.execute("""
CREATE TABLE IF NOT EXISTS iceberg.test_db.users (
    id INT,
    name VARCHAR,
    created_at TIMESTAMP
)
""")

cur.execute("INSERT INTO iceberg.test_db.users VALUES (1, 'Adlo', current_timestamp)")
cur.execute("SELECT * FROM iceberg.test_db.users")

for row in cur.fetchall():
    print(row)