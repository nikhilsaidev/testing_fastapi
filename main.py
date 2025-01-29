from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simulated database
users_db = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
}

# Pydantic model for request validation
class User(BaseModel):
    name: str
    email: str

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Fetch user by ID."""
    if user_id in users_db:
        return users_db[user_id]
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", status_code=201)
def create_user(user: User):
    """Create a new user."""
    user_id = max(users_db.keys(), default=0) + 1
    users_db[user_id] = {"name": user.name, "email": user.email}
    return {"id": user_id, **users_db[user_id]}
