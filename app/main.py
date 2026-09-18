from fastapi import FastAPI, HTTPException, status
from app.schemas import UserCreate
app = FastAPI(title="Lab1 - FastAPI User API")

users: list[UserCreate] = []
@app.get("/health")
def health(): 
    return {"status": "ok"}

@app.get("/hello")
def hello(): 
    return {"message": "Hello World"}
@app.post("/app/users", status_code=status.HTTP_201_CREATED)
def add_user(new_user: UserCreate):
    users.append(new_user)
    return new_user