from fastapi import Depends, FastAPI
from . import models
from .database import engine
from passlib.context import CryptContext
from .routers import user,trip,auth,join
from .config import settings


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(trip.router)
app.include_router(auth.router)
app.include_router(join.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

