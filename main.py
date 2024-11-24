from typing import List
from fastapi import FastAPI, HTTPException
from schema import ToDoCreate, ToDoUpdate, ToDoResponse, ToDoUncompleted
from database.base import session
from database.todo import ToDo

app = FastAPI()


@app.post("/todos/", response_model=ToDoResponse)
async def create_task(todo: ToDoCreate):
    db_todo = ToDo(**todo.dict())
    session.add(db_todo)
    session.commit()
    return db_todo


@app.get("/todos/", response_model=List[ToDoResponse])
async def get_tasks():
    all_tasks = session.query(ToDo).all()
    return all_tasks

@app.get("/todos/{todo_id}/", response_model=ToDoResponse)
async def get_task_by_id(todo_id: int):
    todo = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Task not found")
    return todo

@app.put("/todos/{todo_id}/", response_model=ToDoResponse)
def update_todo(todo_id: int, todo: ToDoUpdate):
    todo_obj = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in todo.dict().items():
        setattr(todo_obj, key, value)
    session.commit()
    session.refresh(todo_obj)
    return todo_obj


@app.delete("/todos/{todo_id}/")
async def delete_task(todo_id: int):
    todo_obj = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(todo_obj)
    session.commit()
    return {"detail": "Todo was deleted successfully"}


@app.get("/todos/uncompleted/", response_model=List[ToDoResponse])
async def get_uncompleted_tasks():
    uncompleted_tasks = session.query(ToDo).filter(ToDo.completed == False).all()
    return uncompleted_tasks

@app.get("/todos/return_completed/", response_model=List[ToDoResponse])
async def get_completed_tasks():
    completed_tasks = session.query(ToDo).filter_by(ToDo.completed == True).all()
    return completed_tasks

@app.put("/todos/{todo_id}/uncompleted/", response_model=ToDoResponse)
def update_todo(todo_id: int, todo: ToDoUncompleted):
    todo_obj = session.query(ToDo).filter(ToDo.id == todo_id).first()
    if not todo_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in todo.dict().items():
        setattr(todo_obj, key, value)
    session.commit()
    session.refresh(todo_obj)
    return todo_obj
