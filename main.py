from fastapi import FastAPI
import models
from database import engine
import routers
import routers.blog
import routers.user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(routers.blog.router)
app.include_router(routers.user.router)
