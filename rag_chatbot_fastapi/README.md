
* * * * *

```
# 🤖 RAG-Based Chatbot with FastAPI, LangGraph & PDF Upload

This project is a **Retrieval-Augmented Generation (RAG) based chatbot** built with **FastAPI**, which allows users to upload any PDF document and then chat with its contents. The system leverages **LangGraph**, **HuggingFace embeddings**, and **FAISS** for powerful document understanding and contextual responses.

---

## 🚀 Features

- 📤 Upload **any PDF** file via FastAPI endpoint
- ✂️ **Split** and **chunk** the document content intelligently
- 🧠 **Embed** content using HuggingFace Transformers
- 🔍 Store embeddings in **FAISS vector store**
- 🤖 **LangGraph chatbot** with memory and context handling
- 🔁 Cookie-based **session tracking**
- 🧹 **Auto-delete PDFs** after processing to save space and protect privacy
- 📡 API endpoints ready for integration with any frontend (React, JS, etc.)

---

## 🧠 How It Works

### 1. Upload Phase
- The user uploads a PDF to `/upload_pdf/`
- Text is extracted from the file using `PyPDF2`
- The text is split into overlapping chunks using `RecursiveCharacterTextSplitter`
- Each chunk is embedded using a **HuggingFace** model (`all-mpnet-base-v2`)
- Vectors are stored in a **FAISS** in-memory index
- A unique **LangGraph chatbot** is created per session

### 2. Chat Phase
- User sends messages to `/chat`
- The chatbot retrieves similar chunks from FAISS
- It builds a prompt and uses **Groq's LLaMA-3.3-70B** (via LangGraph) to generate responses
- Memory is preserved between chats using `MemorySaver`
- Session is tracked via **HTTP cookie** (`session_id`)

---

## 📁 Project Structure

```

rag_chatbot_fastapi/\
├── app/\
│ ├── main.py # FastAPI app instance\
│ ├── api.py # API routes (upload_pdf, chat)\
│ ├── pdf_utils.py # PDF text extraction logic\
│ ├── vector_utils.py # Chunking, embedding, FAISS store\
│ ├── langgraph_flow.py # LangGraph graph + chatbot creation\
├── uploads/ # Temporary PDF upload directory\
├── requirements.txt # All required dependencies\
├── README.md # You're reading this 😉

```

---

## 🔑 Tech Stack

| Purpose            | Tech/Library                                |
|--------------------|---------------------------------------------|
| API framework      | FastAPI                                     |
| PDF parsing        | PyPDF2                                      |
| Text splitting     | LangChain `RecursiveCharacterTextSplitter`  |
| Embeddings         | HuggingFace (`all-mpnet-base-v2`)           |
| Vector store       | FAISS                                       |
| LLM                | Groq's `llama-3.3-70b-versatile` via LangGraph |
| Chat memory        | LangGraph `MemorySaver`                     |
| Session tracking   | FastAPI cookie-based auth                   |

---

## 🧪 API Endpoints

### `POST /upload_pdf/`
Upload your PDF and receive a chatbot session ID via HTTP cookie.

```bash
curl -X POST -F "file=@your_resume.pdf" http://localhost:8000/upload_pdf/

```

### `POST /chat`

Send your message. Cookie `session_id` must be included automatically if using a browser.

```
POST /chat
{
  "message": "What is this document about?"
}

```

* * * * *

🧹 Auto Cleanup
---------------

Uploaded PDFs are **automatically deleted** from the server after embedding is completed --- ensuring low disk usage and user privacy.

* * * * *

🛠️ Setup Instructions
----------------------

1.  ✅ Clone the repo

2.  🔧 Create a virtual environment

3.  📦 Install dependencies

```
pip install -r requirements.txt

```

1.  🔑 Set your Groq API key (you'll need it for LLaMA):

```
export GROQ_API_KEY=your_key_here  # Linux/macOS
set GROQ_API_KEY=your_key_here     # Windows CMD

```

1.  ▶️ Run the server:

```
uvicorn main:app --reload

```

1.  🔍 Open Swagger docs at:\
    `http://127.0.0.1:8000/docs`

* * * * *

✨ Possible Improvements
-----------------------

-   Frontend with chat UI and progress bar (React or HTML/JS)

-   File size validation (e.g., max 5MB)

-   Session timeout and cleanup logic

-   Persistent vector DB (e.g., save FAISS to disk)

-   RAG evaluation metrics (RAGAS)

* * * * *

🙋‍♂️ Author
------------

Built with ❤️ by **Alok** -- AI/ML Researcher & Developer\
If you found this useful, feel free to ⭐ the repo or connect!

