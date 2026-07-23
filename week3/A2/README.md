# Task API (SQLite)

A simple CRUD API built with FastAPI and SQLite.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Data persists after server restarts using SQLite

---

## Technologies

- Python
- FastAPI
- SQLite
- sqlite3

---

## Why SQLite?

SQLite was chosen because it is lightweight, requires no separate database server, and stores all data in a single file. It is ideal for small projects and learning database fundamentals.

---

## Project Structure

```
.
├── main.py
├── database.py
├── models.py
├── tasks.db
└── README.md
```

---

## Database

The database file is automatically created as:

```
tasks.db
```

The application automatically:

- Creates the database if it does not exist.
- Creates the `tasks` table if it does not exist.
- Inserts three sample tasks only on the first run.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/vishalkumarparwani/FlyRank_VishalKmar
cd FlyRank-Assignments/week2
```

Install dependencies:

```bash
pip install fastapi uvicorn
```

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get one task |
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |

---



![Swagger Docs](images/Screenshot%202026-07-24%20001916.png)

![POST Request](images/Screenshot%202026-07-24%20002216.png)