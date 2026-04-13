import sqlite3
import uuid
from pathlib import Path

from platformdirs import user_data_dir


APP_NAME = "OpenCode"
APP_AUTHOR = "OpenCode"


def _db_path() -> Path:
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "history.db"


def init_db() -> None:
    conn = sqlite3.connect(_db_path())
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                model TEXT NOT NULL,
                cloud_provider TEXT NOT NULL,
                workspace TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES sessions(session_id)
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def ensure_session(
    model: str,
    cloud_provider: str,
    workspace: str,
    session_id: str | None = None,
) -> str:
    sid = session_id or str(uuid.uuid4())
    conn = sqlite3.connect(_db_path())
    try:
        conn.execute(
            """
            INSERT OR IGNORE INTO sessions (session_id, model, cloud_provider, workspace)
            VALUES (?, ?, ?, ?)
            """,
            (sid, model, cloud_provider, workspace),
        )
        conn.commit()
        return sid
    finally:
        conn.close()


def add_message(session_id: str, role: str, content: str) -> None:
    conn = sqlite3.connect(_db_path())
    try:
        conn.execute(
            """
            INSERT INTO messages (session_id, role, content)
            VALUES (?, ?, ?)
            """,
            (session_id, role, content),
        )
        conn.commit()
    finally:
        conn.close()


def list_sessions(limit: int = 50) -> list[dict]:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT session_id, model, cloud_provider, workspace, created_at
            FROM sessions
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_session_messages(session_id: str) -> list[dict]:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT role, content, created_at
            FROM messages
            WHERE session_id = ?
            ORDER BY id ASC
            """,
            (session_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
