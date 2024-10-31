from fastapi import FastAPI,Depends
from pydantic import BaseModel
from typing import Optional,List
from models import TodoModel
from database import engine,sessionlocal
from sqlalchemy.orm import Session

app= FastAPI()
TodoModel.metadata.create_all(bind=engine)


class TodoBase(BaseModel):
    title: str
    description : Optional[str]=None
    completed: bool=False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

    class Config:
        orm_mode=True

def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos",response_model=List[TodoResponse])
def get_todos(db: Session=Depends(get_db)):
    todos=db.query(TodoModel).all()
    return todos
 

@app.get("/todos/{todo_id}",response_model=Optional[TodoResponse])
def get_todo(todo_id:int,db: Session=Depends(get_db)):
    todo=db.query(TodoModel).filter(TodoModel.id==todo_id).first()
    return todo

@app.post("/todos",response_model=TodoResponse)
def create_todo(todo:TodoCreate,db:Session=Depends(get_db)):
    todo_db_created=TodoModel(title=todo.title,description=todo.description,completed=todo.completed)
    db.add(todo_db_created)
    db.commit()
    db.refresh(todo_db_created)
    return todo_db_created


@app.delete("/todos/{todo_id}",response_model=TodoResponse)
def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo=db.query(TodoModel).filter(TodoModel.id==todo_id).first()
    db.delete(todo)
    db.commit()
    return todo

