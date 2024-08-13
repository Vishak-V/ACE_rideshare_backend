from fastapi import Depends,Response,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from .. import models,schemas,utils
from fastapi.encoders import jsonable_encoder

router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate,db: Session=Depends(get_db)):
    if "crimson.ua.edu" not in user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Crimson email addresses are allowed")
    hashedPassword=utils.hash(user.password)
    user.password=hashedPassword
    newUser=models.User(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==str(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return jsonable_encoder(user)