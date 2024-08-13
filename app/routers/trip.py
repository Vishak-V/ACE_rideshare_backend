from fastapi import Depends,Response,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from .. import models,schemas,oauth2
from typing import List,Optional

router=APIRouter(
    prefix="/trips",
    tags=["trips"]
)

@router.get("/")
def get_trips(db: Session=Depends(get_db),response_model=List[schemas.Trip],currentUser: int = Depends(oauth2.get_current_user),
              limit:int = 10,skip:int = 0, search:Optional[str]=None):
    
    trips=db.query(models.Trip).limit(limit).offset(skip).all()
    
    #tripsWithSlots=db.query(models.Trip).filter(models.Trip.slotVacant>0).limit(limit).offset(skip).all()

    return trips

@router.get("/{id}")
def get_trip(id: int,db: Session=Depends(get_db),response_model=schemas.Trip,currentUser: int = Depends(oauth2.get_current_user)):
    trip=db.query(models.Trip).filter(models.Trip.id==str(id)).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_trip(trip: schemas.TripCreate,db: Session=Depends(get_db),response_model=schemas.Trip,currentUser: int = Depends(oauth2.get_current_user)):
    newTrip=models.Trip(ownerId=currentUser.id,**trip.model_dump())
    db.add(newTrip)
    db.commit()
    db.refresh(newTrip)
    return newTrip

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(id: int,db: Session=Depends(get_db),currentUser: int = Depends(oauth2.get_current_user)):
    trip=db.query(models.Trip).filter(models.Trip.id==str(id)).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.ownerId!=currentUser.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this trip")
    deletedTrip=db.query(models.Trip).filter(models.Trip.id==str(id)).delete(synchronize_session=False)
    
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Trip)
def update_trip(updatedTrip: schemas.Trip,db: Session=Depends(get_db),currentUser: int = Depends(oauth2.get_current_user)):

    updateQuery=db.query(models.Trip).filter(models.Trip.id==str(id))
    if not updateQuery.first():
        raise HTTPException(status_code=404, detail="Trip not found")
    if updateQuery.first().ownerId!=currentUser.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this trip")
    updatedData=updatedTrip.model_dump()
    updatedData.pop("id",None)
    updateQuery.update(updatedData)
    db.commit()
    return updatedTrip