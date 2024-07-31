import logging

from fastapi import Depends, FastAPI, HTTPException
from geopy.distance import geodesic
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from . import models, schemas

DATABASE_URL = "sqlite:///./address_book.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the actual database tables based on the models.py
models.Base.metadata.create_all(bind=engine)


# Create an instance of the FastAPI class
app = FastAPI()

# Set up logging
logging.basicConfig(filename="app.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def get_db():
    """
    Priovides a database session for each request.
    Closes the session after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    """
    Returns a message indicating that the server is running.
    """
    return {"message": "Hello World"}


@app.post("/addresses/", response_model=schemas.Address, tags=["Address Book"])
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)) -> models.Address:
    """
    Create a new address.
    Returns the created address.
    """
    db_address = models.Address(**address.model_dump())
    try:
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    except IntegrityError as e:
        db.rollback()
        logging.error(f"Create address: {str(e)}")
        raise HTTPException(status_code=400, detail="Address with this latitude and longitude already exists")


@app.get("/addresses/{address_id}", response_model=schemas.Address, tags=["Address Book"])
def read_address(address_id: int, db: Session = Depends(get_db)) -> models.Address:
    """
    Get an address by its ID.
    Returns the address if it exists, otherwise raises a 404 error.
    """
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        logging.error(f"Address with ID {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address


@app.put("/addresses/{address_id}", response_model=schemas.Address, tags=["Address Book"])
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)) -> models.Address:
    """
    Update an address by its ID.
    Returns the updated address if it exists, otherwise raises a 404 error.
    """
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        logging.error(f"Address with ID {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    # db_address.address = address.address
    # db_address.latitude = address.latitude
    # db_address.longitude = address.longitude
    for key, value in address.model_dump().items():
        setattr(db_address, key, value)
    try:
        db.commit()
        db.refresh(db_address)
        return db_address
    except IntegrityError as e:
        db.rollback()
        logging.error(f"Update address: {str(e)}")
        raise HTTPException(status_code=400, detail="Address with this latitude and longitude already exists")


@app.delete("/addresses/{address_id}", tags=["Address Book"])
def delete_address(address_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    """
    Delete an address by its ID.
    Returns a message indicating that the address was deleted if it exists, otherwise raises a 404 error.
    """
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if not db_address:
        logging.error(f"Address with ID {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted"}


@app.get("/addresses/", response_model=list[schemas.Address], tags=["Address Book"])
def read_addresses_within_distance_km(
    latitude: float, longitude: float, distance: float, db: Session = Depends(get_db)
) -> list:
    """
    Get addresses within a given distance from the given location.
    Returns a list of addresses withing the specified distance(km).
    """
    all_addresses = db.query(models.Address).all()
    nearby_addresses = []
    for address in all_addresses:
        # Calculate the distance between the given location and the address
        if geodesic((latitude, longitude), (address.latitude, address.longitude)).km <= distance:
            nearby_addresses.append(address)
    
    return nearby_addresses