# Rest API server with FastAPI and MongoDB
## About
---
Making FARM app server with Python and MongoDB   
A few changes, but basically followed the course   
https://www.udemy.com/course/farm-stack-react-fastapi/   
(The course is taught in Japanese)

## Usage
---
Create your MongoDB database and collection    
  - database: api_db   
  - collection1: users   
  - collection2: todos   

Create .env file and save it under `/server/` directory.
```.env
MONGO_API_KEY=mongodb+srv://<User Name>:<User Password>@<Datebase Name>.<something>.mongodb.net/?retryWrites=true&w=majority
CSRF_KEY=<Your Csrf Key>
JWT_KEY=<Your Jwt Key>
```
Build and Run the container
```shell
docker compose build
```
```shell
docker compose up
``` 
Open your browser and go to http://localhost:8000/ and see `{"message":"Welcome to Fast API"}`   
Go to http://localhost:8000/docs/ and see the API documentation    

## Other  
--- 

Official Doc  
https://fastapi.tiangolo.com

Reference for Dockerizeing FastAPI app
https://github.com/dgonzo27/fastapi-demo
