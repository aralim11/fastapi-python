from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import libs.token
import schemas, models
from fastapi.security import OAuth2PasswordRequestForm
from libs.hashing import Hash
import schemas.login
import schemas.token
from typing import Annotated

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(request: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not (user and Hash.verify(request.password, user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    

    access_token = libs.token.create_access_token(
        data={"sub": user.email}
    )
    return schemas.token.Token(access_token=access_token, token_type="bearer")