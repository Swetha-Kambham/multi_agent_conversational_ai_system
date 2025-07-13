from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from datetime import datetime

# --- Load .env ---
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

# --- MongoDB Setup ---
client = MongoClient(MONGODB_URI)
db = client["hackathon"]
conversations_collection = db["conversations"]

# --- FastAPI App ---
app = FastAPI()

# --- Request Schema ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- Together AI Call ---
def call_mixtral(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post("https://api.together.xyz/inference", headers=headers, json=data)

    print("Status code:", response.status_code)
    print("Response body:", response.text)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["text"].strip()
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Invalid response format from Together API.")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


# --- Root Endpoint ---
@app.get("/")
def root():
    return {"Name": "Swetha Kambham"}

# --- /chat Endpoint ---
@app.post("/chat")
def chat(request: ChatRequest):
    prompt = request.message
    user_id = request.user_id

    # 1. Call LLM
    response = call_mixtral(prompt)

    # 2. Log conversation to MongoDB
    conversations_collection.insert_one({
        "user_id": user_id,
        "message": prompt,
        "response": response,
        "timestamp": datetime.utcnow()
    })

    return {
        "user_id": user_id,
        "message": prompt,
        "response": response
    }
