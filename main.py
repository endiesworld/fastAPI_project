import uuid
from datetime import datetime
from typing import Union, List

from turtle import title
from fastapi import Depends, FastAPI, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from service import all_posts, create_post, delete_one_post, update_one_post, fake_users_db



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def fake_hash_password(password: str):
    return "fakehashed" + password

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    
    
class UserInDB(User):
    hashed_password: str
    

class Post(BaseModel):
    title: str
    content: str
    rating: Union[int, None] = None

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
    
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
    

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_post(token: str = Depends(oauth2_scheme))->List[Post]:
    posts = [Post(**post) for post in all_posts]
    return posts


@app.post("/posts")
async def get_post(post: Post, token: str = Depends(oauth2_scheme)) -> Post:
    post = post.json()
    post["creatAt"] = datetime.now()
    return Post(**post)

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/createposts")
async def createposts(new_post: Post):
    new_post_dict = new_post.dict()
    new_post_dict["id"] = uuid.uuid1()
    created_post = create_post(new_post_dict)
    return {'new_post': created_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: str, response: Response):
    post = delete_one_post(post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post for ID: {post_id}')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{post_id}")
async def update_post(post_id: str, post: Post):
    post = update_one_post(post_id, post.dict())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post for ID: {post_id}')
    return {'post': post}