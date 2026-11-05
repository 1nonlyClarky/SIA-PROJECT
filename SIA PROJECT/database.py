import sqlite3


class Database:

  def __init__(self, db_name="project_data.db"):
    self.db_name = db_name
    self.create_tables()

  def connect(self):
    return sqlite3.connect(self.db_name)

  def create_tables(self):
    conn = self.connect()
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
    conn.commit()
    conn.close()

  def execute_query(self, query, params=()):
    conn = self.connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

  def fetch_one(self, query, params=()):
    conn = self.connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result