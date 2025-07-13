# 🧠 Multi-Agentic Conversational AI System

This is a Python-based RESTful API chatbot powered by the **Mixtral LLM (via Together AI)**, with **Retrieval-Augmented Generation (RAG)** and a custom-built lightweight **CRM system** using MongoDB.

---

## 🚀 Features

✅ Chatbot powered by Together AI's Mixtral model  
✅ RAG: Intelligent document retrieval via FAISS vector store  
✅ Upload documents (PDF, TXT, CSV, JSON)  
✅ Full conversation memory stored per user  
✅ CRM: Create, update, and view user profiles  
✅ Conversation tagging and session tracking  
✅ Conversation reset per user  
✅ RESTful API with FastAPI & Swagger UI

---

## 🧰 Tech Stack

- Python 3.9+
- FastAPI (RESTful API)
- Together AI (Mixtral-8x7B-Instruct-v0.1)
- LangChain + FAISS (RAG pipeline)
- HuggingFace + SentenceTransformers
- MongoDB (via Docker)
- Docker Compose

---

## 📁 Project Structure

```
multi_agent_ai_system/
├── main.py                  # FastAPI backend
├── rag/
│   └── document_handler.py  # Handles upload + chunking + embedding
├── docker-compose.yml       # MongoDB Docker config
├── .env                     # Your API keys and DB URI
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Project

```bash
git clone https://github.com/your-username/multi_agent_ai_system.git
cd multi_agent_ai_system
```

---

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3. Add Environment Variables

Create a `.env` file in the root folder with:

```env
TOGETHER_API_KEY=your_together_api_key_here
MONGODB_URI=mongodb://admin:adminpass@localhost:27017/
```

---

### 4. Start MongoDB (via Docker)

```bash
docker compose up -d
```

---

### 5. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

✅ Open Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📡 API Contracts

All API routes use JSON and follow RESTful principles.

---

### 🔹 `POST /chat`

Accepts user message and returns LLM-generated response with RAG context if relevant.

**Request:**
```json
{
  "user_id": "swetha123",
  "message": "What is the monthly rent for Tia Dalma?"
}
```

**Response:**
```json
{
  "user_id": "swetha123",
  "message": "What is the monthly rent for Tia Dalma?",
  "response": "Tia Dalma’s monthly rent is $115,935.",
  "rag_context_used": "Property: 269 W 39th St, Monthly Rent: $115,935"
}
```

---

### 🔹 `POST /upload_docs`

Uploads a document (PDF, TXT, CSV) and indexes it for retrieval.

**Form Data:**
```
file = HackathonInternalKnowledgeBase.csv
```

**Response:**
```json
{
  "message": "Indexed 225 document chunks from HackathonInternalKnowledgeBase.csv"
}
```

---

### 🔹 `POST /crm/create_user`

Creates a new user profile in the CRM.

**Request:**
```json
{
  "user_id": "swetha123",
  "name": "Swetha Kambham",
  "email": "swethakambham75@gmail.com",
  "company": "OpenAI",
  "preferences": "AI assistant"
}
```

---

### 🔹 `PUT /crm/update_user`

Updates an existing user profile.

**Request:**
```json
{
  "user_id": "swetha123",
  "name": "Swetha",
  "email": "swetha@example.com"
}
```

---

### 🔹 `GET /crm/conversations/{user_id}`

Returns all previous conversation messages for a given user.

**Response:**
```json
{
  "user_id": "swetha123",
  "conversations": [
    {
      "message": "What is Mixtral?",
      "response": "Mixtral is a model by Mistral AI..."
    }
  ]
}
```

---

### 🔹 `POST /reset`

Deletes all conversation messages for a given user.

**Request:**
```json
{
  "user_id": "swetha123"
}
```

**Response:**
```json
{
  "message": "Deleted 8 conversation(s) for user swetha123"
}
```

---

## 🧪 Testing

You can test endpoints using:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Postman: import the endpoints and send JSON requests

---

## 💡 Optional Enhancements

- Add `tags` field to conversations (`"resolved"`, `"follow-up"`)
- Add calendar event hooks (Google Calendar API)
- Export conversations as PDF
- Frontend chatbot using React, Vue, or Streamlit

---

## 👩‍💻 Built By

**Swetha Kambham**  
📧 swethakambham75@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/swetha-kambham-564096140/)

---

## ✅ Submission Checklist

- [x] Working chatbot using Together API
- [x] RAG with FAISS + Document Upload
- [x] Full CRM (create/update users, store chats)
- [x] All REST API endpoints complete
- [x] `.env` file support
- [x] README with API contract & setup