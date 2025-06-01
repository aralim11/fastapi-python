from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schemas.blog import Blog
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

 
@app.get("/")
def getData():
    return {"message": "Hello, World 2!"}

@app.get("/blog/{id}")
def show(id: int):
    return {"data": id}

@app.post("/blog")
def createBlog(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, description=blog.description, published=blog.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}