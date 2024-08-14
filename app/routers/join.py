from fastapi import Depends,Response,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from .. import models,schemas,oauth2
from typing import List,Optional

router=APIRouter(
    prefix="/join",
    tags=["join"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def join_trip(join: schemas.Join,db: Session=Depends(get_db),currentUser: int = Depends(oauth2.get_current_user)):
    trip=db.query(models.Trip).filter(models.Trip.id==join.tripId).first()
    group_query=db.query(models.Join).filter(models.Join.userId==currentUser.id).filter(models.Join.tripId==join.tripId)
    group=group_query.first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    if  join.dir==1:
        if trip.ownerId==currentUser.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You cannot join your own trip")
        if trip.slotVacant<=0:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This trip is already full")
        if trip.checkedBagLimit<join.checkBags:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have too many checked bags")
        if trip.carryOnLimit<join.carryOnBags:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have too many carry on bags")
        
        if group:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already joined this trip")
        if db.query(models.Join).filter(models.Join.userId==currentUser.id).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already joined a trip")
        db.query(models.Trip).filter(models.Trip.id==join.tripId).update({"slotVacant": trip.slotVacant-1})
        db.query(models.Trip).filter(models.Trip.id==join.tripId).update({"checkedBagLimit": trip.checkedBagLimit-join.checkBags})
        db.query(models.Trip).filter(models.Trip.id==join.tripId).update({"carryOnLimit": trip.carryOnLimit-join.carryOnBags})
        new_group=models.Join(userId=currentUser.id,tripId=join.tripId)
        db.add(new_group)
        db.commit()
        return{"message":"You have successfully joined the trip"}
    else:
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not joined this trip")
        group_query.delete(synchronize_session=False)
        db.query(models.Trip).filter(models.Trip.id==join.tripId).update({"slotVacant": trip.slotVacant+1})
        db.commit()

        return {"message":"You have successfully left the trip"}

