

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Walk the dog", "done": False},
    {"id": 3, "title": "Finish assignment", "done": True},
]

next_id = 4

def get_all():
    return tasks


def get_by_id(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def create_task(newTitle: str, isDone: bool):
    global next_id

    if newTitle == '':
        return None

    new_task = {}
    new_task["id"] = next_id
    new_task["title"] = newTitle
    new_task["done"] = isDone

    tasks.append(new_task)
    next_id += 1

    return new_task


def update_task(task_id: int, newTitle: str, isDone: bool):
    for task in tasks:
        if task["id"] == task_id:
            if newTitle != '':
                task["title"] = newTitle
            task["done"] = isDone
            return task
    return None


def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return None