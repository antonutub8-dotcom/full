import aiosqlite
from datetime import datetime
from config import DB_PATH


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                created_at TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_key TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                file_type TEXT DEFAULT 'text',
                file_id TEXT DEFAULT '',
                created_at TEXT
            )
            """
        )
        await db.commit()


async def add_user(user_id: int, username: str | None, full_name: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, full_name, created_at) VALUES (?, ?, ?, ?)",
            (user_id, username or "", full_name, datetime.now().isoformat()),
        )
        await db.commit()


async def get_all_users() -> list[tuple[int]]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cur:
            return await cur.fetchall()


async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            users_count = (await cur.fetchone())[0]
        async with db.execute(
            "SELECT category_key, COUNT(*) FROM items GROUP BY category_key"
        ) as cur:
            rows = await cur.fetchall()
    return {"users": users_count, "by_category": dict(rows)}


async def add_item(
    category_key: str,
    title: str,
    description: str = "",
    file_type: str = "text",
    file_id: str = "",
) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO items (category_key, title, description, file_type, file_id, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (
                category_key,
                title,
                description,
                file_type,
                file_id,
                datetime.now().isoformat(),
            ),
        )
        await db.commit()
        return cur.lastrowid


async def get_items_by_category(category_key: str) -> list[tuple]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, title, description, file_type, file_id FROM items"
            " WHERE category_key = ? ORDER BY id",
            (category_key,),
        ) as cur:
            return await cur.fetchall()


async def get_item(item_id: int) -> tuple | None:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, category_key, title, description, file_type, file_id FROM items WHERE id = ?",
            (item_id,),
        ) as cur:
            return await cur.fetchone()


async def delete_item(item_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM items WHERE id = ?", (item_id,))
        await db.commit()


async def find_item_by_text(category_key: str | None, text: str) -> tuple | None:
    """Поиск позиции по точному названию (без учета регистра)."""
    text_clean = text.strip().lower()
    async with aiosqlite.connect(DB_PATH) as db:
        if category_key:
            query = (
                "SELECT id, category_key, title, description, file_type, file_id FROM items"
                " WHERE category_key = ? AND lower(title) = ? LIMIT 1"
            )
            params = (category_key, text_clean)
        else:
            query = (
                "SELECT id, category_key, title, description, file_type, file_id FROM items"
                " WHERE lower(title) = ? LIMIT 1"
            )
            params = (text_clean,)
        async with db.execute(query, params) as cur:
            return await cur.fetchone()
