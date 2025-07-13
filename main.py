from fastapi import FastAPI
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client["hackathon"]
users_collection = db["users"]
conversations_collection = db["conversations"]

# FastAPI app
app = FastAPI()

@app.get("/chat")
def root():
    return {"Swetha Kambham"}
