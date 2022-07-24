# Rest API server with FastAPI and MongoDB
## About
Making FARM app server with Python and MongoDB   
A few changes, but basically followed the course   
https://www.udemy.com/course/farm-stack-react-fastapi/   
(The course is taught in Japanese)

## Run container in local
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
Build and Run the container in local
```shell
docker compose up --build
```
Open your browser and go to http://localhost:8000/ and see `{"message":"Welcome to Fast API"}`   
Go to http://localhost:8000/docs/ and see the API documentation    

## Run Fast API in local
For the first time, you need to change the permission
```zsh
# Root
chmod 700 scripts/local_run.sh
```
Run script by command below
```zsh
# Root
./scripts/local_run.sh
```
Then access to http://127.0.0.1:8000   
You can see `{"message":"Welcome to Fast API"}` at the page
## Activate to / Deactivate from virtual env
```shell
# /server/
# Activate
source env_api/bin/activate

# Deactivate
deactivate
```

## Build and Push the image to ECR
```shell
bash deploy.sh
```

## Other  

Official Doc  
https://fastapi.tiangolo.com

Reference for Dockerizeing FastAPI app
https://github.com/dgonzo27/fastapi-demo

Heroku CLI
https://devcenter.heroku.com/articles/heroku-cli