from http import client
from typing import Collection
from decouple import config
from typing import Union
import motor.motor_asyncio

MONGO_API_KEY=config('MONGO_API_KEY')
client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)

db = client.API_DB
cll_todos = db.todos
cll_users = db.users

def todo_serializer(todo: dict) -> dict:
  return {
    'id': str(todo['_id']), # convert ObjectId to string
    'title': todo['title'],
    'completed': todo['completed']
  }

async def insert_todo(todo: dict) -> Union[dict, bool]:
  todo = await cll_todos.insert_one(todo)
  new_todo = await cll_todos.find_one({'_id': todo.inserted_id})
  if(new_todo):
    return todo_serializer(new_todo)
  return False