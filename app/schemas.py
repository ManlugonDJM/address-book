from pydantic import BaseModel, Field

class AddressCreate(BaseModel):
    address: str
    latitude: float = Field(..., gt=-90, lt=90, description="Latitude must be between -90 and 90.")
    longitude: float = Field(..., gt=-180, lt=180, description="Longitude must be between -180 and 180.")


class AddressUpdate(AddressCreate):
    ...

class Address(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float

    class Config:
        # orm_mode = True # for Pydantic 1.0
        from_attributes = True # for Pydantic 2.0