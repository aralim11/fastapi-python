from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from schemas.blog import Blog
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

 
@app.get("/blog", status_code=status.HTTP_200_OK)
def getData(response: Response, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"data": blogs}

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    return {"data": blog}

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def createBlog(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, description=blog.description, published=blog.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}