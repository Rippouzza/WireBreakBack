from sqlalchemy.orm import Session
from models.supplier import Supplier

def get_all_suppliers(db: Session):
    """Retrieve all suppliers from the database."""
    return db.query(Supplier).all()

def get_supplier_by_id(db: Session, supplier_id: str):
    """Retrieve a specific supplier by ID."""
    return db.query(Supplier).filter(Supplier.supplierid == supplier_id).first()

def create_supplier(db: Session, supplier_id: str):
    """Create a new supplier (ID auto-generated)."""
    new_supplier = Supplier(supplierid=supplier_id)
    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)
    return new_supplier

def delete_supplier(db: Session, supplier_id: str):
    """Delete a supplier by ID."""
    supplier = db.query(Supplier).filter(Supplier.supplierid == supplier_id).first()
    if supplier:
        db.delete(supplier)
        db.commit()
        return True
    return False

def update_supplier(db: Session, supplier_id: str, new_supplier_id: str):
    """Update a supplier's details by ID."""
    supplier = db.query(Supplier).filter(Supplier.supplierid == supplier_id).first()
    if supplier:
        supplier.supplierid = new_supplier_id  # Assuming only supplierid is updated
        db.commit()
        db.refresh(supplier)
        return supplier
    return None
