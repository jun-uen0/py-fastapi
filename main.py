from fastapi import FastAPI
from routers import route_todos, route_auth
from schemas import SuccessMsg

app = FastAPI()
app.include_router(route_todos.router)
app.include_router(route_auth.router)

@app.get("/", response_model=SuccessMsg) # Responce Type: SuccessMsg
def root():
  return {"message": "← defined in schemas.py"}
