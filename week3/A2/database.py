import sqlite3

DATABASE = "tasks.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM tasks")

    if cur.fetchone()[0] == 0:
        cur.executemany(
            """
            INSERT INTO tasks(title, done)
            VALUES (?, ?)
            """,
            [
                ("Buy milk", 0),
                ("Walk the dog", 0),
                ("Finish assignment", 1),
            ],
        )

    conn.commit()
    cur.close()
    conn.close()


def get_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, done FROM tasks")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []

    for row in rows:
        result.append(
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"]),
            }
        )

    return result


def get_by_id(task_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,),
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return None

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
    }


def create_task(new_title: str, is_done: bool):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks(title, done)
        VALUES (?, ?)
        """,
        (new_title, int(is_done)),
    )

    conn.commit()

    new_id = cur.lastrowid

    cur.close()
    conn.close()

    return {
        "id": new_id,
        "title": new_title,
        "done": is_done,
    }


def update_task(task_id: int, new_title: str, is_done: bool):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (new_title, int(is_done), task_id),
    )

    conn.commit()

    if cur.rowcount == 0:
        cur.close()
        conn.close()
        return None

    cur.close()
    conn.close()

    return {
        "id": task_id,
        "title": new_title,
        "done": is_done,
    }


def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )

    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()

    return deleted