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
    for existing_user in users:
        if existing_user.userid == new_user.userid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="A user with this id already exists")
    users.append(new_user)
    return new_user