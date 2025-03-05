from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.machine_type_service import (
    get_all_machine_types, get_machine_type_by_name, create_machine_type, update_machine_type, delete_machine_type
)

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
machine_type_bp = Blueprint('machine_type_bp', __name__)

@machine_type_bp.route('/machinetypes', methods=['GET'])
def list_machine_types():
    """Get all machine types."""
    db = SessionLocal()
    machine_types = get_all_machine_types(db)
    db.close()
    return jsonify([{
        "machinetype": mt.machinetype,
        "minBreakDiameter": mt.minBreakDiameter,
        "maxBreakDiameter": mt.maxBreakDiameter
    } for mt in machine_types]), 200

@machine_type_bp.route('/machinetypes/<string:machinetype>', methods=['GET'])
def get_machine_type(machinetype):
    """Get a machine type by name."""
    db = SessionLocal()
    machine_type = get_machine_type_by_name(db, machinetype)
    db.close()
    if machine_type:
        return jsonify({
            "machinetype": machine_type.machinetype,
            "minBreakDiameter": machine_type.minBreakDiameter,
            "maxBreakDiameter": machine_type.maxBreakDiameter
        }), 200
    return jsonify({"error": "Machine type not found"}), 404

@machine_type_bp.route('/machinetypes', methods=['POST'])
def add_machine_type():
    """Create a new machine type."""
    db = SessionLocal()
    machine_type_data = request.json
    machine_type = create_machine_type(db, machine_type_data)
    db.close()
    return jsonify({
        "machinetype": machine_type.machinetype,
        "minBreakDiameter": machine_type.minBreakDiameter,
        "maxBreakDiameter": machine_type.maxBreakDiameter
    }), 201

@machine_type_bp.route('/machinetypes/<string:machinetype>', methods=['PUT'])
def modify_machine_type(machinetype):
    """Update an existing machine type's details."""
    db = SessionLocal()
    try:
        update_data = request.json
        updated_machine_type = update_machine_type(db, machinetype, update_data)
        if updated_machine_type:
            response_data = {
                "machinetype": updated_machine_type.machinetype,
                "minBreakDiameter": updated_machine_type.minBreakDiameter,
                "maxBreakDiameter": updated_machine_type.maxBreakDiameter
            }
            db.close()
            return jsonify(response_data), 200
        db.close()
        return jsonify({"error": "Machine type not found"}), 404
    except Exception as e:
        db.rollback()
        db.close()
        return jsonify({"error": str(e)}), 500

@machine_type_bp.route('/machinetypes/<string:machinetype>', methods=['DELETE'])
def remove_machine_type(machinetype):
    """Delete a machine type by name."""
    db = SessionLocal()
    success = delete_machine_type(db, machinetype)
    db.close()
    if success:
        return jsonify({"message": "Machine type deleted successfully"}), 200
    return jsonify({"error": "Machine type not found"}), 404
