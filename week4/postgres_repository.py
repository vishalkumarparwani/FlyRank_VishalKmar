from db import get_connection

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({"id": row[0], "title": row[1], "done": row[2]})
    return result

def get_by_id(task_id):
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
    rows = cur.fetchone()
    cur.close()
    conn.close()

    if rows is None:
        return None

    return {"id": rows[0], "title": rows[1], "done": rows[2]}


def create_task(new_title: str, is_done: bool):
    if new_title.strip() == '':
        return None
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
        (new_title, is_done)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"id": new_id, "title": new_title, "done": is_done}


def update_task(task_id: int, new_title: str, is_done: bool):
    if new_title.strip() == '':
        return None
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
        (new_title, is_done, task_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        return None
    
    return {"id": row[0], "title": row[1], "done": row[2]}


def delete_task(task_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id", (task_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        return False
    
    return True