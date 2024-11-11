from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="User Management Service")

class User(BaseModel):
    name: str
    email: str

users_db = {}
user_id_counter = 1

@app.get("/api/users")
def list_users():
    return list(users_db.values())

@app.post("/api/users")
def create_user(user: User):
    global user_id_counter
    user_id = user_id_counter
    user_id_counter += 1
    
    new_user = {
        "id": user_id,
        "name": user.name,
        "email": user.email
    }
    users_db[user_id] = new_user
    return new_user

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
