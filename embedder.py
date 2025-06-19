import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema.document import Document

def load_python_files(repo_root):
    documents = []
    for root, _, files in os.walk(repo_root):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    loader = TextLoader(path, encoding="utf-8")
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"⚠️ Skipped {path}: {e}")
    return documents

def chunk_and_embed(documents, persist_directory="db"):
    # Split documents into manageable chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    # Load a Hugging Face embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Store in ChromaDB
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return vectordb
