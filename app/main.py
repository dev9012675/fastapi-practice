from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel 

class Post(BaseModel):
    title:str
    content : str | None = None

app = FastAPI()
posts = []

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data":posts}

@app.get('/posts/{id}')
async def get_post(id:int):
    post = await find_post(id)
    if post:
        return {"data":post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')
    

@app.post('/posts' , status_code= status.HTTP_201_CREATED)
async def create_post(post: Post):
   post = post.model_dump()
   if len(posts) == 0:
       post['id'] = 1
   else:
       post['id'] = (posts[-1])['id'] + 1
   posts.append(post)
   return {'data':post}

@app.put('/posts/{id}')
async def update_post(id:int , post:Post):
    index =  await find_index(id)
    if index != None:
        post = post.model_dump()
        post["id"] = id
        posts[index] = post
        return {"data":post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')



@app.delete('/posts/{id}' , status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(id:int):
    index =  await find_index(id)
    if index != None:
        posts.pop(index)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post does not exist.')



async def find_post(id):
    for post in posts:
        if post["id"] == id:
            return post
    return None

async def find_index(id):
    for index , post in enumerate(posts):
        print(post)
        print(index)
        if post["id"] == id:
            return index
    return None

