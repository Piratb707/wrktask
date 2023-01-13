from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# Определяем схему безопасности OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Определяем модель регистрации пользователя
class UserRegistration(BaseModel):
    username: str
    password: str

# Определяем модель для входа пользователя
class UserLogin(BaseModel):
    username: str
    password: str

# Определяем модель поста
class Post(BaseModel):
    title: str
    content: str

# Определяем базу данных (для демонстрационных целей это просто python dict)
users = {"test": {"password": "password123", "posts": []}}

# Определяем маршруты
@app.post("/signup")
async def signup(user: UserRegistration):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    users[user.username] = {"password": user.password, "posts": []}
    return {"message": "User created"}

@app.post("/login")
async def login(user: UserLogin):
    if user.username not in users or user.password != users[user.username]["password"]:
        raise HTTPException(status_code=400, detail="Invalid login")
    return {"message": "Login successful"}

@app.post("/post")
async def create_post(post: Post, user: str = Depends(oauth2_scheme)):
    users[user]["posts"].append(post.dict())
    return {"message": "Post created"}

@app.get("/post")
async def read_post(user: str = Depends(oauth2_scheme)):
    return {"posts": users[user]["posts"]}

@app.put("/post/{post_id}")
async def update_post(post_id: int, post: Post, user: str = Depends(oauth2_scheme)):
    users[user]["posts"][post_id] = post.dict()
    return {"message": "Post updated"}

@app.delete("/post/{post_id}")
async def delete_post(post_id: int, user: str = Depends(oauth2_scheme)):
    del users[user]["posts"][post_id]
    return {"message": "Post deleted"}
