from fastapi import FastAPI, HTTPException, status, Response, Depends
from app.schemas import UserCreate, UserRead

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.models import Base, UserDB

from sqlalchemy import select


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


@app.get("/api/users", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    statement = select(UserDB).order_by(UserDB.id)
    return db.execute(statement).scalars().all()

@app.get("/api/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(UserDB, user_id)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    db.delete(db_user)
    db.commit()
    return
