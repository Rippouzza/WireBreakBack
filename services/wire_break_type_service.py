from sqlalchemy.orm import Session
from models.wire_break_type_model import WireBreakType

def get_all_wire_break_types(db: Session):
    """Retrieve all wire break types from the database."""
    return db.query(WireBreakType).all()

def get_wire_break_type_by_name(db: Session, wirebreaktype: str):
    """Retrieve a specific wire break type by its name."""
    return db.query(WireBreakType).filter(WireBreakType.wirebreaktype == wirebreaktype).first()

def create_wire_break_type(db: Session, wire_break_type_data: dict):
    """Create a new wire break type."""
    wire_break_type = WireBreakType(**wire_break_type_data)
    db.add(wire_break_type)
    db.commit()
    db.refresh(wire_break_type)
    return wire_break_type

def update_wire_break_type(db: Session, wirebreaktype: str, update_data: dict):
    """Update an existing wire break type's details."""
    wire_break_type = db.query(WireBreakType).filter(WireBreakType.wirebreaktype == wirebreaktype).first()
    if wire_break_type:
        for key, value in update_data.items():
            setattr(wire_break_type, key, value)
        db.commit()
        db.refresh(wire_break_type)
        return wire_break_type
    return None

def delete_wire_break_type(db: Session, wirebreaktype: str):
    """Delete a wire break type by name."""
    wire_break_type = db.query(WireBreakType).filter(WireBreakType.wirebreaktype == wirebreaktype).first()
    if wire_break_type:
        db.delete(wire_break_type)
        db.commit()
        return True
    return False
