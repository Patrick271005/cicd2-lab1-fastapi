from fastapi import FastAPI, HTTPException, status, Response, Depends
from app.schemas import UserCreate, UserRead

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, UserDB


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lab1 - FastAPI User API")

users: list[UserCreate] = []
@app.get("/health")
def health(): 
    return {"status": "ok"}

@app.get("/hello")
def hello(): 
    return {"message": "Hello World"}

@app.post("/api/users", status_code=status.HTTP_201_CREATED ,response_model=UserRead)
def add_user(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**new_user.model_dump())
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="A user with this email or student_id already exists",
        )
    return db_user


@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for existing_user in users:
        if existing_user.user_id == user_id:
            return existing_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )




@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    # Use enumerate so we can find the user and remove it by index.
    for index, existing_user in enumerate(users):
        if existing_user.user_id == user_id:
            users.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )
