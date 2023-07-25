from typing import Optional, List
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()
users = []


class User(BaseModel):
    email: str
    is_active: bool
    bio: Optional[str] = None


@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post("/users")
async def create_user(user: User):
    users.append(user)
    return users


@app.get("/users/{id}")
async def get_user(id: int = Path(..., description="The ID of the user you want to retrieve", gt=2)):
    return users[id]
