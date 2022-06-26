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

async def db_update_single_todo(id: str, data: dict) -> Union[dict, bool]:
  todo = await cll_todos.find_one({'_id': ObjectId(id)})
  if todo: 
    # continue if todo is not None
    updated_todo = await cll_todos.update_one( 
      # update_one() return UpdateResult class
      {'_id': ObjectId(id)}, {"$set": data}
    )
    if updated_todo.modified_count > 0: 
      # UpdateResult class has modified_count attribute
      # If the modified_count is larger than zero, the update was successful
      new_todo = await cll_todos.find_one({"_id": ObjectId(id)})
      return todo_serializer(new_todo)
  return False

async def db_delete_single_todo(id: str) -> bool:
  todo = await cll_todos.delete_one({'_id': ObjectId(id)})
  if todo:
    deleted_todo = await cll_todos.delete_one( 
      # update_one() return UpdateResult class
      {'_id': ObjectId(id)}
    )
    if deleted_todo.deleted_count > 0:
      # UpdateResult class has deleted_count attribute
      # If the deleted_count is larger than zero, the delete was successful
      return True
  return False