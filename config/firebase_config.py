import os
import firebase_admin
from firebase_admin import credentials

# Get the absolute path of the Django project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR: {BASE_DIR}")  # Debug print to verify the path

# Path to Firebase key
cred_path = os.path.join(BASE_DIR, "config", "firebase-admin-key.json")

# Initialize Firebase only if not already done
if not firebase_admin._apps:
    # Check if the file exists before trying to load it
    if not os.path.exists(cred_path):
        raise FileNotFoundError(
            f"Firebase credentials file not found at: {cred_path}\n"
            f"Please ensure 'firebase-admin-key.json' exists in the config directory."
        )
    
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase initialized successfully")