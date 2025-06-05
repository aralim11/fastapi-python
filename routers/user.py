from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
import schemas.user
from database import get_db
from libs.hashing import Hash

router = APIRouter(
    tags=["User"]
)

## create user
@router.post("/user", status_code=status.HTTP_201_CREATED)
def createUser(request: schemas.user.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}

## get all users
@router.get("/users", status_code=status.HTTP_200_OK)
def users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")

    return {"data": all_users}

## get user by ID
@router.get("/user/{id}", status_code=status.HTTP_200_OK)
def getUserByID(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")
    
    return {"data": user}