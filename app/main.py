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
@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for existing_user in users:
        if existing_user.userid == user_id:
            return existing_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        details="User not found",
    )




#@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
#def delete_user(user_id: int):
    # Use enumerate so we can find the user and remove it by index.
    #for index, existing_user in enumerate(users):
        #if existing_user.user_id == user_id:
            #users.pop(index)
        #return Response(status_code=status.HTTP_204_NO_CONTENT)
#raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found",)
