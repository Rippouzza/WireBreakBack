from sqlalchemy.orm import Session
from models.plant import Plant

def get_all_plants(db: Session):
    """Retrieve all plants from the database."""
    return db.query(Plant).all()

def create_plant(db: Session, plant_data: dict):
    """Create a new plant entry."""
    new_plant = Plant(**plant_data)
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant

def update_plant(db: Session, plant_name: str, update_data: dict):
    """Update an existing plant's details."""
    plant = db.query(Plant).filter(Plant.Plant == plant_name).first()
    if plant:
        for key, value in update_data.items():
            setattr(plant, key, value)
        db.commit()
        db.refresh(plant)  # ✅ Ensure the object stays attached to the session
        return plant
    return None

def delete_plant(db: Session, plant_name: str):
    """Delete a plant entry by its name."""
    plant = db.query(Plant).filter(Plant.Plant == plant_name).first()
    if plant:
        db.delete(plant)
        db.commit()
        return True
    return False
