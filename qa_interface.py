from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
import os
from dotenv import load_dotenv

load_dotenv()

def load_vectorstore(persist_directory="db"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb

from langchain_google_genai import ChatGoogleGenerativeAI

def build_qa_chain():
    vectordb = load_vectorstore()

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    return qa

