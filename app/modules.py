import sqlite3
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()

DB_PATH = 'db/portfolio.db'  # Ensure this path is correct

# Database connection function
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables dictionary-style access
    return conn

class User(UserMixin):
    def __init__(self, id, username, email, password, bio=None, phone=None, language=None, two_factor=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.phone = phone
        self.language = language
        self.two_factor = two_factor

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    @staticmethod
    def get_user_by_username(username):
        """Fetch user by username."""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()
        if user:
            # Accessing the fields directly from the Row object
            return User(user['id'], user['username'], user['email'], user['password'], user['bio'], user['phone'], user['language'], user['two_factor'])
        return None

    @staticmethod
    def get_user_by_email(email):
        """Fetch user by email."""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        if user:
            # Accessing the fields directly from the Row object
            return User(user['id'], user['username'], user['email'], user['password'], user['bio'], user['phone'], user['language'], user['two_factor'])
        return None

    @staticmethod
    def get_user_by_id(user_id):
        """Fetch user by ID."""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
        if user:
            # Accessing the fields directly from the Row object
            return User(user['id'], user['username'], user['email'], user['password'], user['bio'], user['phone'], user['language'], user['two_factor'])
        return None

    @staticmethod
    def update_user_info(user_id, username, email, bio, phone, language):
        """Update user info."""
        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("""
                UPDATE users
                SET username = ?, email = ?, bio = ?, phone = ?, language = ?
                WHERE id = ?
            """, (username, email, bio, phone, language, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False

    @staticmethod
    def update_user_password(user_id, password):
        """Update user password."""
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                UPDATE users
                SET password = ?
                WHERE id = ?
            """, (hashed_pw, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False

    @staticmethod
    def update_user_2fa(user_id, two_factor):
        """Update user two-factor authentication setting."""
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                UPDATE users
                SET two_factor = ?
                WHERE id = ?
            """, (two_factor, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False

    @staticmethod
    def register_user(username, email, password):
        """Register a new user."""
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, hashed_pw))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False  # Username or email already exists
        except Exception as e:
            conn.close()
            return False


def init_db():
    """Creates the database and users table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            bio TEXT,
            phone TEXT,
            language TEXT,
            two_factor TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
