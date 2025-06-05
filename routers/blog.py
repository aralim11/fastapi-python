from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas.blog

router = APIRouter()

## get all blogs
@router.get("/blog", status_code=status.HTTP_200_OK, tags=['Blog'])
def getData(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return {"data": blogs}

## get blog by ID
@router.get("/blog/{id}", status_code=status.HTTP_200_OK, tags=['Blog'])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    return {"data": blog}

## create blog
@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blog'])
def createBlog(blog: schemas.blog.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, description=blog.description, published=blog.published, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}

## update blog
@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def blogUpdate(id, request: schemas.blog.Blog ,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    blog.update({'title': request.title, 'description': request.description, 'published': request.published})
    db.commit()
    return {"data": "Updated"}

## delete blog
@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def deleteBlog(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Blog not deleted")
    