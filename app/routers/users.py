from fastapi import APIRouter
from app.models.user import User
from app.database.fake_db import users_db

router = APIRouter()

@router.get("/users")
def get_users():
    return users_db

@router.post("/users")
def create_user(user: User):
    users_db.append(user)
    return user

@router.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    return {"error": "User not found"}


@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return {"message": "User deleted"}
    return {"error": "User not found"}

@router.put("/users/{user_id}")
def put_user(user_id: int, name_user: str):
    for user in users_db:
        if user.id == user_id:
            user.name = name_user   # ← aquí está la corrección importante
            return {
                "message": "User updated",
                "data": user
            }
    return {"error": "User not found"}
