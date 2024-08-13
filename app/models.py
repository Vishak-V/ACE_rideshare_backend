from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Trip(Base):
    __tablename__ = "trips"
    id = Column(String, primary_key=True, index=True)
    dateCreated = Column(TIMESTAMP(timezone=True))
    pickUpTime = Column(TIMESTAMP(timezone=True))
    dropOffTime = Column(TIMESTAMP(timezone=True))
    dropOffLocation = Column(String)
    pickUpLocation = Column(String)
    slotLimit = Column(Integer)
    slotVacant = Column(Integer)
    checkedBagLimit = Column(Integer)
    carryOnLimit = Column(Integer)
    costPerPerson = Column(Float)
    Notes = Column(String)
    ownerId = Column(String,ForeignKey('users.id', ondelete="CASCADE"),nullable=False)

    owner=relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    firstName = Column(String)
    lastName = Column(String)
    dateCreated = Column(TIMESTAMP(timezone=True))
    class config:
        orm_mode=True

class UserTrip(Base):
    __tablename__ = "user_trips"
    userId = Column(String,ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    tripId = Column(String,ForeignKey('trips.id', ondelete="CASCADE"), primary_key=True)
    class config:
        orm_mode=True
   