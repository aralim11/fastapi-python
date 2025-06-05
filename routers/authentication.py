from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import libs.token
import schemas, models
import schemas.login
from libs.hashing import Hash
import schemas.token

router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(request: schemas.login.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not (user and Hash.verify(request.password, user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    

    access_token = libs.token.create_access_token(
        data={"sub": user.email}
    )
    return schemas.token.Token(access_token=access_token, token_type="bearer")