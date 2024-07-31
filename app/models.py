from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
    """
    Defines the Address model for the database.
    Each address has an ID, address, latitude, and longitude.
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Add a unique constraint for lat and long so no duplicate addresses can be created
    __table_args__ = (UniqueConstraint("latitude", "longitude", name='_latitude_longitude_uc'),)