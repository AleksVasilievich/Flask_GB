'''
Необходимо создать API для управления списком задач.
Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
GET /tasks — возвращает список всех задач.
GET /tasks/{id} — возвращает задачу с указанным идентификатором.
POST /tasks — добавляет новую задачу.
PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Модель данных для задачи
class Task(BaseModel):
    title: str
    description: str
    status: bool

# Хранилище задач (замените этот код на работу с базой данных или другим хранилищем)
tasks = []

# Конечная точка для получения списка всех задач
@app.get("/tasks", response_model=List[Task])
async def read_tasks():
    return tasks

# Конечная точка для создания новой задачи
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

# Конечная точка для получения задачи по идентификатору
@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return tasks[task_id]

# Конечная точка для обновления задачи по идентификатору
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    tasks[task_id] = task
    return task

# Конечная точка для удаления задачи по идентификатору
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    deleted_task = tasks.pop(task_id)
    return deleted_task