from model import Todo

import motor.motor_asyncio  # MongoDB driver

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

database = client.Todolist
collection = database.todo


async def fetch_one(title):
    document = await collection.find_one({"title": title})
    return document


async def fetch_all():
    todos = []
    current = collection.find({})
    async for document in current:
        todos.append(Todo(**document))
    return todos


async def create_todo(todo):
    document = todo
    final = await collection.insert_one(document)
    return document


async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document


async def delete_todo(title):
    response = await collection.delete_one({"title": title})
    return response
