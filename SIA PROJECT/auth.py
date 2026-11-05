import hashlib
import os
import sqlite3


class AuthManager:

  def __init__(self, db):
    self.db = db

  def hash_password(self, password, salt=None):
    if salt is None:
      salt = os.urandom(16).hex()
    salted_password = (salt + password).encode("utf-8")
    password_hash = hashlib.sha256(salted_password).hexdigest()
    return password_hash, salt

  def register_user(self, username, password):
    if not username or not password:
      return False, "Please fill in all fields."
    if len(password) < 4:
      return False, "Password must be at least 4 characters."

    password_hash, salt = self.hash_password(password)
    try:
      self.db.execute_query(
          "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
          (username, password_hash, salt),
      )
      return True, "Registration successful! You can now log in."
    except sqlite3.IntegrityError:
      return False, "Username already exists. Pick another one."

  def verify_login(self, username, password):
    if not username or not password:
      return False, "Please enter both username and password."

    user_record = self.db.fetch_one(
        "SELECT password_hash, salt FROM users WHERE username = ?", (username,)
    )

    if not user_record:
      return False, "Invalid username or password."

    stored_hash, salt = user_record
    entered_hash, _ = self.hash_password(password, salt)

    if entered_hash == stored_hash:
      return True, f"Welcome, {username}!"
    return False, "Invalid username or password."