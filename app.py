from flask import Flask
from flask_cors import CORS  # Import the CORS extension
from controllers.file_upload_controller import upload_file
from controllers.auth_controller import authenticate  # Import authentication controller
from controllers.supplier_controller import supplier_bp  # Import the supplier blueprint

app = Flask(__name__)

# Enable CORS for all routes, allowing requests from your frontend (Angular)
CORS(app, origins="http://localhost:4200")  # Replace with your frontend URL if different

# Register the supplier blueprint
app.register_blueprint(supplier_bp, url_prefix='/api')  # Register with a URL prefix

@app.route('/')
def home():
    return "Welcome to the WireBreak file upload API!"

@app.route('/upload', methods=['POST'])
def upload_file_route():
    return upload_file()

@app.route('/authenticate', methods=['POST'])
def authenticate_route():
    return authenticate()

if __name__ == '__main__':
    app.run(debug=True)
