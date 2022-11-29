from typing import Union
import uuid

from turtle import title
from fastapi import Response, FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

all_posts = [{"title": "post_one", "content": "content for post one", "id": "1", "rating": 4}, 
             {"title": "post_two", "content": "content for post two", "id": "2", "rating": 3}]

class Post(BaseModel):
    title: str
    content: str
    rating: Union[int, None] = None

def create_post(post):
    all_posts.append(post)
    return post
    
def get_one_post(id):
    post = [post for post in all_posts if post["id"] == id]
    if len(post) > 0 :
        return post[0]
    return None

def delete_one_post(id):
    post_index = None
    deleted_post = None
    for index, post in enumerate(all_posts):
        if post["id"] == id:
            post_index = index
            deleted_post = post
            break
    if post_index is not None:
        all_posts.pop(post_index)
    return deleted_post

def update_one_post(post_id, update_post):
    post_index = None
    for index, post in enumerate(all_posts):
        if post["id"] == post_id:
            post_index = index
            break
    if post_index is not None:
        all_posts[post_index]["title"] =  update_post["title"]   
        all_posts[post_index]["content"] =  update_post["content"] 
        return all_posts[post_index]
    return None

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_post():
    return {'post': all_posts}

@app.get("/posts/{post_id}")
async def get_post(post_id: str, response: Response):
    post = get_one_post(post_id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f'No post for ID: {post_id}'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post for ID: {post_id}')
    return {'post': post}


@app.post("/post", status_code=status.HTTP_201_CREATED)
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