# app/vector_utils.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss

def chunk_and_embed_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.create_documents([text])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    dim = len(embeddings.embed_query("hello world"))

    index = faiss.IndexFlatL2(dim)
    
    store = FAISS(
        embedding_function=embeddings, 
        index=index, 
        docstore=InMemoryDocstore(), 
        index_to_docstore_id={})
    store.add_documents(docs)
    return store

def store_vectorstore(session_id, store):
    store.save_local(f"db/{session_id}")
