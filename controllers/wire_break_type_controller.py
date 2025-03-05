from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.wire_break_type_service import (
    get_all_wire_break_types, get_wire_break_type_by_name, create_wire_break_type,
    update_wire_break_type, delete_wire_break_type
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
wire_break_type_bp = Blueprint('wire_break_type_bp', __name__)

@wire_break_type_bp.route('/wirebreaktypes', methods=['GET'])
def list_wire_break_types():
    """Get all wire break types."""
    db = SessionLocal()
    wire_break_types = get_all_wire_break_types(db)
    db.close()
    return jsonify([{
        "wirebreaktype": wbt.wirebreaktype,
        "typeB": wbt.typeB
    } for wbt in wire_break_types]), 200

@wire_break_type_bp.route('/wirebreaktypes/<string:wirebreaktype>', methods=['GET'])
def get_wire_break_type(wirebreaktype):
    """Get a wire break type by name."""
    db = SessionLocal()
    wire_break_type = get_wire_break_type_by_name(db, wirebreaktype)
    db.close()
    if wire_break_type:
        return jsonify({
            "wirebreaktype": wire_break_type.wirebreaktype,
            "typeB": wire_break_type.typeB
        }), 200
    return jsonify({"error": "Wire break type not found"}), 404

@wire_break_type_bp.route('/wirebreaktypes', methods=['POST'])
def add_wire_break_type():
    """Create a new wire break type."""
    db = SessionLocal()
    wire_break_type_data = request.json
    wire_break_type = create_wire_break_type(db, wire_break_type_data)
    db.close()
    return jsonify({
        "wirebreaktype": wire_break_type.wirebreaktype,
        "typeB": wire_break_type.typeB
    }), 201

@wire_break_type_bp.route('/wirebreaktypes/<string:wirebreaktype>', methods=['PUT'])
def modify_wire_break_type(wirebreaktype):
    """Update an existing wire break type's details."""
    db = SessionLocal()
    try:
        update_data = request.json
        updated_wire_break_type = update_wire_break_type(db, wirebreaktype, update_data)
        if updated_wire_break_type:
            response_data = {
                "wirebreaktype": updated_wire_break_type.wirebreaktype,
                "typeB": updated_wire_break_type.typeB
            }
            db.close()
            return jsonify(response_data), 200
        db.close()
        return jsonify({"error": "Wire break type not found"}), 404
    except Exception as e:
        db.rollback()
        db.close()
        return jsonify({"error": str(e)}), 500

@wire_break_type_bp.route('/wirebreaktypes/<string:wirebreaktype>', methods=['DELETE'])
def remove_wire_break_type(wirebreaktype):
    """Delete a wire break type by name."""
    db = SessionLocal()
    success = delete_wire_break_type(db, wirebreaktype)
    db.close()
    if success:
        return jsonify({"message": "Wire break type deleted successfully"}), 200
    return jsonify({"error": "Wire break type not found"}), 404
