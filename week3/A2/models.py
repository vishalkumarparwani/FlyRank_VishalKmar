from pydantic import BaseModel

class Task(BaseModel):
    title: str
    done: bool = False