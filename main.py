from fastapi import FastAPI
from schemas.blog import Blog

app = FastAPI()

 
@app.get("/")
def getData():
    return {"message": "Hello, World 2!"}

@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}

@app.post("/blog")
def createBlog(blog: Blog):
    return {"message": f"Blog created {blog.title}"}