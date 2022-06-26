from http import client
from typing import Collection
from decouple import config
from typing import Union
from bson import ObjectId
import motor.motor_asyncio

MONGO_API_KEY=config('MONGO_API_KEY')
client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)

db = client.FastAPI01
cll_todos = db.todos
cll_users = db.users

def todo_serializer(todo: dict) -> dict:
  return {
    "id": str(todo["_id"]),
    "title": todo["title"],
    "description": todo["description"]
  }

async def db_create_todo(todo: dict) -> Union[dict, bool]:
  todo = await cll_todos.insert_one(todo)
  new_todo = await cll_todos.find_one({'_id': todo.inserted_id})
  if new_todo:
    return todo_serializer(new_todo)
  return False

async def db_get_todos() -> list:
  todos = []
  for todo in await cll_todos.find().to_list(length=100): # to_list() gets all the documents in the collection
    todos.append(todo_serializer(todo))
  return todos

async def db_get_single_todo(id: str) -> Union[dict, bool]:
  todo = await cll_todos.find_one({'_id': ObjectId(id)})
  if todo:
    return todo_serializer(todo)
  return False