import os
import sqlite3


def main():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "database.db")
    if not os.path.exists(db_path):
        print(f"SQLite file not found: {db_path}")
        return
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:")
    for t in tables:
        print(f"- {t}")
    con.close()


if __name__ == "__main__":
    main()


