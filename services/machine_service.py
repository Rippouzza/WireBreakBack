from sqlalchemy.orm import Session
from models.machine import Machine
from models.machine_type_model import MachineType

def get_all_machines(db: Session):
    """Retrieve all machines from the database."""
    return db.query(Machine).all()

def get_machine_by_code(db: Session, code_machine: str):
    """Retrieve a specific machine by its code."""
    return db.query(Machine).filter(Machine.codeMachine == code_machine).first()

def create_machine(db: Session, machine_data: dict):
    """Create a new machine after verifying typeM exists."""
    
    # Check if typeM exists in machinetype table
    type_exists = db.query(MachineType).filter(MachineType.machinetype == machine_data["typeM"]).first()
    if not type_exists:
        return {"error": f"Machine type '{machine_data['typeM']}' does not exist. Add it to machinetype first."}, 400
    
    machine = Machine(**machine_data)
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine


def update_machine(db: Session, code_machine: str, update_data: dict):
    """Update an existing machine's details."""
    machine = db.query(Machine).filter(Machine.codeMachine == code_machine).first()
    if machine:
        for key, value in update_data.items():
            setattr(machine, key, value)  # Apply changes dynamically
        db.commit()  # Commit changes
        db.refresh(machine)  # Refresh to keep session bound
        return machine  # Return updated object while session is still open
    return None

def delete_machine(db: Session, code_machine: str):
    """Delete a machine by its code."""
    machine = db.query(Machine).filter(Machine.codeMachine == code_machine).first()
    if machine:
        db.delete(machine)
        db.commit()
        return True
    return False
