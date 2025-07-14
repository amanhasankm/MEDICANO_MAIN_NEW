from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["pill_reminder"]
    collection = db["reminders"]
    
    # Try a simple command to check connection
    client.admin.command("ping")
    print(" MongoDB connected successfully!")
except Exception as e:
    print(f" MongoDB connection failed: {e}")

def save_medicine(name, dose, phone, time):
    doc = {"name": name, "dose": dose, "phone": phone, "time": time}
    collection.insert_one(doc)

def get_all_reminders():
    return list(collection.find())
