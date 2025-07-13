from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import requests
from datetime import datetime
from fastapi import File, UploadFile
from rag.document_handler import ingest_documents
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from typing import Optional

# --- Load .env ---
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")

# --- MongoDB Setup ---
client = MongoClient(MONGODB_URI)
db = client["hackathon"]
conversations_collection = db["conversations"]
users_collection = db["users"]

# Create User Schema
class User(BaseModel):
    user_id: str
    name: str
    email: str
    company: Optional[str] = None
    preferences: Optional[str] = None


# --- FastAPI App ---
app = FastAPI()

# --- Request Schema ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- Together AI Call ---
def call_mixtral(user_question: str, context: str = "") -> str:
    prompt = f"""You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question: {user_question}

Answer:"""

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

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["text"].strip()
        except (KeyError, IndexError):
            raise HTTPException(status_code=500, detail="Invalid response format from LLM.")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


# --- Root Endpoint ---
@app.get("/")
def root():
    return {"Name": "Swetha Kambham"}

# --- /chat Endpoint ---
@app.post("/chat")
def chat(request: ChatRequest):
    user_id = request.user_id
    user_query = request.message

    # 🧠 RAG: Retrieve relevant chunks from FAISS
    rag_context = ""
    if os.path.exists("rag_index"):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("rag_index", embeddings, allow_dangerous_deserialization=True)
        results = db.similarity_search(user_query, k=3)
        rag_context = "\n\n".join([doc.page_content for doc in results])
    else:
        print("No RAG index found. Proceeding without context.")

    # 🤖 Call LLM with injected context
    response = call_mixtral(user_query, context=rag_context)

    # 🗃️ Log to MongoDB
    conversations_collection.insert_one({
        "user_id": user_id,
        "message": user_query,
        "response": response,
        "context": rag_context,
        "timestamp": datetime.utcnow()
    })

    return {
        "user_id": user_id,
        "message": user_query,
        "response": response,
        "rag_context_used": rag_context[:500]  # Optional: return part of the context
    }

# --- /upload_docs Endpoint ---
@app.post("/upload_docs")
async def upload_docs(file: UploadFile = File(...)):
    # Save uploaded file locally
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    try:
        num_chunks = ingest_documents(file_location)
    except ValueError as e:
        os.remove(file_location)
        raise HTTPException(status_code=400, detail=str(e))

    os.remove(file_location)
    return {"message": f"Indexed {num_chunks} document chunks from {file.filename}"}

# --- /crm/create_user Endpoint ---
@app.post("/crm/create_user")
def create_user(user: User):
    if users_collection.find_one({"user_id": user.user_id}):
        raise HTTPException(status_code=400, detail="User already exists.")
    
    users_collection.insert_one(user.dict())
    return {"message": f"User {user.user_id} created successfully."}

# --- /crm/update_user Endpoint ---
@app.put("/crm/update_user")
def update_user(user: User):
    result = users_collection.update_one(
        {"user_id": user.user_id},
        {"$set": user.dict()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"message": f"User {user.user_id} updated successfully."}

# --- /crm/conversations{user_id}/ ---
@app.get("/crm/conversations/{user_id}")
def get_conversations(user_id: str):
    convs = list(conversations_collection.find({"user_id": user_id}, {"_id": 0}))
    return {"user_id": user_id, "conversations": convs}
