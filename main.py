from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.blog import Blog
from schemas.user import User
import models
from database import engine, get_db
from libs.hashing import Hash

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

## get all blogs
@app.get("/blog", status_code=status.HTTP_200_OK)
def getData(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"data": blogs}

## get blog by ID
@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    return {"data": blog}

## create blog
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def createBlog(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, description=blog.description, published=blog.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}

## update blog
@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def blogUpdate(id, request: Blog ,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    blog.update({'title': request.title, 'description': request.description, 'published': request.published})
    db.commit()
    return {"data": "Updated"}

## delete blog
@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Blog not deleted")
    

## create user
@app.post("/user", status_code=status.HTTP_201_CREATED)
def createUser(request: User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}