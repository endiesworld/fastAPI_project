from fastapi import Body, FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_post():
    return {'post': 'This is post message'}


@app.post("/createposts")
async def createposts(payload: dict = Body(...)):
    print(payload)
    return {'message': 'Post created successfuly'}
