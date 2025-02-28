from sqlalchemy.orm import Session
from models.role import Role
import logging

# Configure logger
logger = logging.getLogger(__name__)

def authenticate_user(db: Session, user_id: str, password: str):
    """Checks if the given ID and password match an Admin role."""
    try:
        user = db.query(Role).filter_by(ID=user_id).first()
        if not user:
            return {"message": "Authentication failed: User not found"}, 401

        # Compare plaintext password directly
        if user.Password != password:
            return {"message": "Authentication failed: Incorrect password"}, 401

        # Check if the user is an Admin
        if user.Role.lower() == "admin":
            return {"message": "Authentication successful: Admin access granted"}, 200
        else:
            return {"message": "Authentication failed: User is not an Admin"}, 403

    except Exception as e:
        logger.error(f"Error during authentication: {str(e)}")
        return {"message": "Internal server error"}, 500
