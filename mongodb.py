from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["smart_attendance"]

students_collection = db["students"]
attendance_collection = db["attendance"]

print("✅ MongoDB Connected")