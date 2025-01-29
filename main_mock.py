from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Simulating a Database Class
class Database:
    def __init__(self):
        self.users = {1: {"name": "Alice", "email": "alice@example.com"}}

    def get_user(self, user_id):
        return self.users.get(user_id)

    def create_user(self, user_data):
        user_id = max(self.users.keys(), default=0) + 1
        self.users[user_id] = user_data
        return {"id": user_id, **user_data}

db = Database()

class User(BaseModel):
    name: str
    email: str

@app.get("/users/{user_id}")
def get_user(user_id: int, database: Database = Depends(lambda: db)):
    """Retrieve user by ID"""
    user = database.get_user(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
def create_user(user: User, database: Database = Depends(lambda: db)):
    """Create a new user"""
    return database.create_user(user.model_dump())
