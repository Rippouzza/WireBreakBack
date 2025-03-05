from sqlalchemy.orm import Session
from models.machine_type_model import MachineType

def get_all_machine_types(db: Session):
    """Retrieve all machine types from the database."""
    return db.query(MachineType).all()

def get_machine_type_by_name(db: Session, machinetype: str):
    """Retrieve a specific machine type by its name."""
    return db.query(MachineType).filter(MachineType.machinetype == machinetype).first()

def create_machine_type(db: Session, machine_type_data: dict):
    """Create a new machine type."""
    machine_type = MachineType(**machine_type_data)
    db.add(machine_type)
    db.commit()
    db.refresh(machine_type)
    return machine_type

def update_machine_type(db: Session, machinetype: str, update_data: dict):
    """Update an existing machine type's details."""
    machine_type = db.query(MachineType).filter(MachineType.machinetype == machinetype).first()
    if machine_type:
        for key, value in update_data.items():
            setattr(machine_type, key, value)
        db.commit()
        db.refresh(machine_type)
        return machine_type
    return None

def delete_machine_type(db: Session, machinetype: str):
    """Delete a machine type by name."""
    machine_type = db.query(MachineType).filter(MachineType.machinetype == machinetype).first()
    if machine_type:
        db.delete(machine_type)
        db.commit()
        return True
    return False
