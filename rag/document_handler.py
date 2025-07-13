from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
import os

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_and_split(file_path: str):
    # Select loader based on file type
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    elif file_path.endswith(".csv"):
        loader = CSVLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(docs)

def ingest_documents(file_path: str):
    chunks = load_and_split(file_path)
    if not os.path.exists("rag_index"):
        db = FAISS.from_documents(chunks, embedding_model)
    else:
        db = FAISS.load_local("rag_index", embedding_model)
        db.add_documents(chunks)
    db.save_local("rag_index")
    return len(chunks)
