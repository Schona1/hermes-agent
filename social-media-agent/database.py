import sqlite3
from config import DATABASE_PATH


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                topic TEXT,
                telegram_message_id INTEGER,
                post_url TEXT,
                posted_time TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                used_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def save_post(platform, content, topic, status="pending"):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO posts (platform, content, topic, status) VALUES (?, ?, ?, ?)",
            (platform, content, topic, status)
        )
        conn.commit()
        return cursor.lastrowid


def get_post(post_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
        return dict(row) if row else None


def update_post_status(post_id, status, telegram_message_id=None, post_url=None, posted_time=None):
    with get_connection() as conn:
        updates = ["status = ?"]
        values = [status]
        if telegram_message_id is not None:
            updates.append("telegram_message_id = ?")
            values.append(telegram_message_id)
        if post_url is not None:
            updates.append("post_url = ?")
            values.append(post_url)
        if posted_time is not None:
            updates.append("posted_time = ?")
            values.append(posted_time)
        values.append(post_id)
        conn.execute(f"UPDATE posts SET {', '.join(updates)} WHERE id = ?", values)
        conn.commit()


def update_post_content(post_id, content):
    with get_connection() as conn:
        conn.execute("UPDATE posts SET content = ? WHERE id = ?", (content, post_id))
        conn.commit()


def get_pending_posts():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM posts WHERE status = 'pending' ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def get_recent_posts(limit=10):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def mark_topic_used(topic):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO topics (topic) VALUES (?)",
            (topic,)
        )
        conn.commit()


def get_used_topics(limit=30):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT topic FROM topics ORDER BY used_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [r["topic"] for r in rows]
