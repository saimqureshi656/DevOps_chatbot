import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_groq import ChatGroq 
from langchain.chains import RetrievalQA
from fastapi import FastAPI 
import streamlit as st
import chromadb

sys.path.append('../..')
if "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]
else:
    
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the PDF file
pdf_path = os.path.join(current_dir, "DevOps_Documentation.pdf")

#loader = PyPDFLoader ('C:/Users/WAJIZ.PK/Desktop/Python_projects/DevOps_bot/DevOps_Documentation.pdf')
loader = PyPDFLoader (pdf_path)

pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    separators= ["/n", "/n/n", " "],
    chunk_size = 1000,
    chunk_overlap = 150,
    length_function = len
    )

docs = text_splitter.split_documents(pages)

#print(len(pages))

import shutil
# Define ChromaDB storage path (Relative for Streamlit Cloud)
#persist_directory = "./Chroma"  # ✅ Works on Streamlit Cloud

embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

chroma_client = chromadb.PersistentClient(path="./chroma_db")

vectordb = Chroma.from_documents(
    documents=docs,  # ✅ Required argument
    embedding=embedding,
    persist_directory=persist_directory
)

#print(vectordb._collection.count())

from langchain.prompts import PromptTemplate
#building prompt
template = """Use the following pieces of context to answer the question at the end. 

- If the user greets (e.g., "hello", "hi", "hey"), respond with a warm greeting like hello, how can i help you today and ask user to provide question regarding DevOps
- If the user says goodbye (e.g., "bye", "goodbye", "see you"), respond with a friendly farewell.  
- If you don't know the answer, just say that you don't know, don't try to make up an answer.  
- Use four sentences maximum. Keep the answer as concise as possible.  
- Always say "Thanks for asking!" at the end unless it's a farewell.     
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)


llm = ChatGroq(
    groq_api_key = os.getenv('GROQ_API_KEY'),
    model_name = 'llama-3.2-3b-preview')


qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=False,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} 
)
