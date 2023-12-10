from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo

app = FastAPI()

from db import (
    fetch_one,
    fetch_all,
    create_todo,
    update_todo,
    delete_todo
)

origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return "Hey there"


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all()
    return response


@app.get("/api/todo{id}", response_model=Todo)
async def get_todo(title):
    response = await fetch_one(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title: {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "Bad Request")


@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title: {title}")


@app.delete("/api/todo{title}")
async def delete_todo_route(title: str):
    response = await delete_todo(title)
    if response.deleted_count == 1:
        return "Successfully deleted!"
    else:
        raise HTTPException(status_code=404, detail=f"There is no todo with the title: {title}")
