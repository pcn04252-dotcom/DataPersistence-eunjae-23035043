import sqlite3


def create_item(conn: sqlite3.Connection, name: str, quantity: int) -> int:
    cursor = conn.execute(
        "INSERT INTO items (name, quantity) VALUES (?, ?)", (name, quantity)
    )
    conn.commit()
    return cursor.lastrowid


def get_item(conn: sqlite3.Connection, item_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id, name, quantity FROM items WHERE id = ?", (item_id,)
    ).fetchone()


def list_items(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT id, name, quantity FROM items ORDER BY id").fetchall()


def update_item(conn: sqlite3.Connection, item_id: int, name: str, quantity: int) -> None:
    conn.execute(
        "UPDATE items SET name = ?, quantity = ? WHERE id = ?",
        (name, quantity, item_id),
    )
    conn.commit()


def delete_item(conn: sqlite3.Connection, item_id: int) -> None:
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
