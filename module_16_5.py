from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel


app = FastAPI()

# Установка папки с шаблонами
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/', response_class=HTMLResponse, summary="Get all users")
async def get_users(request: Request):
    """
    Retrieve a list of all users.
    """
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get('/users/{user_id}', response_class=HTMLResponse, summary="Get a user by ID")
async def get_user(request: Request, user_id: Annotated[int, Path(description='Enter User ID', ge=1)]):
    """
    Retrieve a user by ID.
    """
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")

@app.post('/user/{username}/{age}', response_model=User, summary="Add a new user")
async def add_user(
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20)],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120)]
):
    """
    Add a new user with the specified username and age.

    - **username**: The username of the new user (5-20 characters).
    - **age**: The age of the new user (18-120).
    """
    max_id = max((user.id for user in users), default=0)
    new_id = max_id + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}', response_model=User, summary="Update a user")
async def update_user(
    user_id: Annotated[int, Path(description='Enter User ID', ge=1)],
    username: Annotated[str, Path(description='Enter username', min_length=5, max_length=20)],
    age: Annotated[int, Path(description='Enter age', ge=18, le=120)]
):
    """
    Update an existing user with the specified user ID, username, and age.

    - **user_id**: The ID of the user to update.
    - **username**: The new username (5-20 characters).
    - **age**: The new age (18-120).
    """
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}', summary="Delete a user", status_code=204)
async def delete_user(
    user_id: Annotated[int, Path(description='Enter User ID', ge=1)]
):
    """
    Delete an existing user with the specified user ID.

    - **user_id**: The ID of the user to delete.
    """
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="User was not found")