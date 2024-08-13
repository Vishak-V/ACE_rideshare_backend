from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    firstName: str
    lastName: str
    dateCreated:datetime
    class config:
        orm_mode=True
    def from_datetime(cls, dt: datetime):
        return cls(dateCreated=dt.isoformat())

class Trip(BaseModel):
    id: str
    dateCreated: str
    pickUpTime: str
    dropOffTime: str
    dropOffLocation: str
    pickUpLocation: str
    slotLimit: int
    slotVacant: int
    checkedBagLimit: int
    carryOnLimit: int
    costPerPerson: float
    Notes: Optional[str] = None
    ownerId: str
    owner:UserResponse
    class config:
        orm_mode=True

class TripCreate(BaseModel):
    id: str
    dateCreated: datetime
    pickUpTime: datetime
    dropOffTime: datetime
    dropOffLocation: str
    pickUpLocation: str
    slotLimit: int
    slotVacant: int
    checkedBagLimit: int
    carryOnLimit: int
    costPerPerson: float
    Notes: Optional[str] = None
    class config:
        orm_mode=True

class UserCreate(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    dateCreated: datetime
    class config: 
        orm_mode=True



class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class config:
        orm_mode=True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userId: Optional[str]=None
    class config:
        orm_mode=True   

class Join(BaseModel):
    tripId: str
    dir: int
    class config:
        orm_mode=True