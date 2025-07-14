import bcrypt
from pymongo import MongoClient
import os
# Connect to MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["medicano"]
users_collection = db["users"]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Checking password
def check_password(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')  # Convert stored string back to bytes
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(username, email, password):
    if users_collection.find_one({"username": username}):
        return False, "Username already exists."
    hashed = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed
    })
    return True, "Registration successful!"

def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and check_password(password, user['password']):
        return True, user
    return False, "Invalid credentials"
