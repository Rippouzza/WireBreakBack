from flask import Flask
from flask_cors import CORS  
from controllers.file_upload_controller import upload_file
from controllers.auth_controller import authenticate
from controllers.plant_controller import plant_bp  # Import plant routes
from controllers.supplier_controller import supplier_bp  # Import supplier routes
from controllers.machine_controller import machine_bp
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins="http://localhost:4200")

@app.route('/')
def home():
    return "Welcome to the WireBreak API!"

@app.route('/upload', methods=['POST'])
def upload_file_route():
    return upload_file()

@app.route('/authenticate', methods=['POST'])
def authenticate_route():
    return authenticate()

# Register blueprints
app.register_blueprint(plant_bp, url_prefix='/api')
app.register_blueprint(supplier_bp, url_prefix='/api')
app.register_blueprint(machine_bp, url_prefix='/api')
if __name__ == '__main__':
    app.run(debug=True)
