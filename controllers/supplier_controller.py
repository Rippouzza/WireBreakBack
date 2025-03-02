from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.supplier_service import get_all_suppliers, get_supplier_by_id, create_supplier, delete_supplier, update_supplier

# Database connection setup
DB_SERVER = 'PC-GHILEB'
DB_NAME = 'WireBreak'
DB_USER = ''
DB_PASSWORD = ''

# SQLAlchemy connection string (Windows Authentication)
conn_str = f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Blueprint
supplier_bp = Blueprint('supplier_bp', __name__)

@supplier_bp.route('/suppliers', methods=['GET'])
def list_suppliers():
    """Get all suppliers."""
    db = SessionLocal()
    suppliers = get_all_suppliers(db)
    db.close()
    return jsonify([{"supplierid": s.supplierid} for s in suppliers]), 200

@supplier_bp.route('/suppliers/<string:supplier_id>', methods=['PUT'])
def update_supplier_route(supplier_id: str):
    """Update a supplier by ID."""
    new_supplier_id = request.json.get('supplierid')
    if not new_supplier_id:
        return jsonify({"error": "New supplier ID is required"}), 400

    db = SessionLocal()
    supplier = update_supplier(db, supplier_id, new_supplier_id)
    db.close()
    if supplier:
        return jsonify({"supplierid": supplier.supplierid}), 200
    return jsonify({"error": "Supplier not found"}), 404

@supplier_bp.route('/suppliers', methods=['POST'])
def add_supplier():
    """Create a new supplier."""
    supplier_id = request.json.get('supplierid')
    if not supplier_id:
        return jsonify({"error": "Supplier ID is required"}), 400
    
    db = SessionLocal()
    supplier = create_supplier(db, supplier_id)
    db.close()
    return jsonify({"supplierid": supplier.supplierid}), 201

@supplier_bp.route('/suppliers/<string:supplier_id>', methods=['DELETE'])
def remove_supplier(supplier_id: str):
    """Delete a supplier by ID."""
    db = SessionLocal()
    success = delete_supplier(db, supplier_id)
    db.close()
    if success:
        return jsonify({"message": "Supplier deleted successfully"}), 200
    return jsonify({"error": "Supplier not found"}), 404
