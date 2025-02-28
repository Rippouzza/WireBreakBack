from flask import request, jsonify
from services.auth_service import authenticate_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database connection setup
DB_SERVER = 'PC-GHILEB'
DB_NAME = 'WireBreak'
DB_USER = ''
DB_PASSWORD = ''

# SQLAlchemy connection string
conn_str = f'mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def authenticate():
    """Controller for user authentication."""
    data = request.json
    user_id = data.get("ID")
    password = data.get("Password")

    if not user_id or not password:
        return jsonify({"message": "Missing ID or Password"}), 400

    db = SessionLocal()
    response, status = authenticate_user(db, user_id, password)
    db.close()

    return jsonify(response), status
