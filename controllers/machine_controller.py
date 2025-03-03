from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.machine_service import (
    get_all_machines, get_machine_by_code, create_machine, update_machine, delete_machine
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
machine_bp = Blueprint('machine_bp', __name__)

@machine_bp.route('/machines', methods=['GET'])
def list_machines():
    """Get all machines."""
    db = SessionLocal()
    machines = get_all_machines(db)
    db.close()
    return jsonify([{"codeMachine": m.codeMachine, "typeM": m.typeM} for m in machines]), 200

@machine_bp.route('/machines/<string:code_machine>', methods=['GET'])
def get_machine(code_machine):
    """Get a machine by code."""
    db = SessionLocal()
    machine = get_machine_by_code(db, code_machine)
    db.close()
    if machine:
        return jsonify({"codeMachine": machine.codeMachine, "typeM": machine.typeM}), 200
    return jsonify({"error": "Machine not found"}), 404

@machine_bp.route('/machines', methods=['POST'])
def add_machine():
    """Create a new machine."""
    db = SessionLocal()
    machine_data = request.json
    machine = create_machine(db, machine_data)
    db.close()
    return jsonify({"codeMachine": machine.codeMachine, "typeM": machine.typeM}), 201

@machine_bp.route('/machines/<string:code_machine>', methods=['PUT'])
def modify_machine(code_machine):
    """Update an existing machine's details."""
    db = SessionLocal()
    try:
        update_data = request.json
        updated_machine = update_machine(db, code_machine, update_data)
        if updated_machine:
            response_data = {
                "codeMachine": updated_machine.codeMachine,
                "typeM": updated_machine.typeM
            }
            db.close()  # Close after ensuring JSON response is prepared
            return jsonify(response_data), 200
        db.close()
        return jsonify({"error": "Machine not found"}), 404
    except Exception as e:
        db.rollback()  # Rollback transaction on error
        db.close()
        return jsonify({"error": str(e)}), 500

@machine_bp.route('/machines/<string:code_machine>', methods=['DELETE'])
def remove_machine(code_machine):
    """Delete a machine by code."""
    db = SessionLocal()
    success = delete_machine(db, code_machine)
    db.close()
    if success:
        return jsonify({"message": "Machine deleted successfully"}), 200
    return jsonify({"error": "Machine not found"}), 404
