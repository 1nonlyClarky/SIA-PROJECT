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
    # Users table for Authentication[cite: 1]
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)
    # Scores table for Games Leaderboard[cite: 1]
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                category TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
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

  def fetch_all(self, query, params=()):
    conn = self.connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

  def save_score(self, username, category, score, total=10):
    self.execute_query(
        "INSERT INTO scores (username, category, score, total) VALUES (?,"
        " ?, ?, ?)",
        (username, category, score, total),
    )

  def get_top_scores(self, limit=8):
    return self.fetch_all(
        "SELECT username, category, score, total, timestamp FROM scores "
        "ORDER BY score DESC, id DESC LIMIT ?",
        (limit,),
    )