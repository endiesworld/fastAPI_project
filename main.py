from turtle import title
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_post():
    return {'post': 'This is post message'}


# @app.post("/createposts")
# async def createposts(payload: dict = Body(...)):
#     print(payload)
#     return {'new_post': payload}

@app.post("/createposts")
async def createposts(new_post: Post):
    print(new_post)
    return {'new_post': new_post}
