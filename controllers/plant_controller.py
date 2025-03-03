from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.plant_service import get_all_plants, create_plant, update_plant, delete_plant

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
plant_bp = Blueprint('plant_bp', __name__)

@plant_bp.route('/plants', methods=['GET'])
def list_plants():
    """Get all plants."""
    db = SessionLocal()
    plants = get_all_plants(db)
    db.close()
    return jsonify([
        {
            "Plant": p.Plant,
            "Region": p.Region,
            "Sales_Company": p.Sales_Company,
            "Inv_Company": p.Inv_Company,
            "plant_Description": p.plant_Description
        }
        for p in plants
    ]), 200

@plant_bp.route('/plants', methods=['POST'])
def add_plant():
    """Create a new plant."""
    db = SessionLocal()
    plant_data = request.json
    new_plant = create_plant(db, plant_data)
    db.close()
    return jsonify({
        "Plant": new_plant.Plant,
        "Region": new_plant.Region,
        "Sales_Company": new_plant.Sales_Company,
        "Inv_Company": new_plant.Inv_Company,
        "plant_Description": new_plant.plant_Description
    }), 201

@plant_bp.route('/plants/<string:plant_name>', methods=['PUT'])
def modify_plant(plant_name):
    """Update an existing plant's details."""
    db = SessionLocal()
    try:
        update_data = request.json
        updated_plant = update_plant(db, plant_name, update_data)
        if updated_plant:
            response_data = {
                "Plant": updated_plant.Plant,
                "Region": updated_plant.Region,
                "Sales_Company": updated_plant.Sales_Company,
                "Inv_Company": updated_plant.Inv_Company,
                "plant_Description": updated_plant.plant_Description
            }
            db.close()  # ✅ Close session only after JSON creation
            return jsonify(response_data), 200
        db.close()
        return jsonify({"error": "Plant not found"}), 404
    except Exception as e:
        db.rollback()
        db.close()
        return jsonify({"error": str(e)}), 500

@plant_bp.route('/plants/<string:plant_name>', methods=['DELETE'])
def remove_plant(plant_name):
    """Delete a plant by its name."""
    db = SessionLocal()
    success = delete_plant(db, plant_name)
    db.close()
    if success:
        return jsonify({"message": "Plant deleted successfully"}), 200
    return jsonify({"error": "Plant not found"}), 404
