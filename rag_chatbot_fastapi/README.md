🤖 RAG-Based Chatbot with FastAPI, LangGraph & PDF Upload
=========================================================

This project is a **Retrieval-Augmented Generation (RAG) based chatbot** built entirely using **FastAPI** and **LangGraph**, designed to allow users to upload their PDF documents and chat with the content intelligently.

It uses modern tools and libraries such as HuggingFace Transformers for embeddings, FAISS for vector search, LangGraph for agent-based orchestration, and Groq's LLaMA-3.3-70B model for generating accurate and contextual responses.

🚀 Features
-----------

*   Upload any PDF file
    
*   Extract text automatically using PyPDF2
    
*   Split and chunk the document using RecursiveCharacterTextSplitter
    
*   Generate sentence embeddings using HuggingFace model all-mpnet-base-v2
    
*   Store embedded chunks into FAISS vector store
    
*   Run a LangGraph-powered chatbot with retrieval and memory
    
*   Track sessions using cookies (auto-generated session\_id)
    
*   Automatically delete uploaded PDF files after processing
    
*   API endpoints are frontend-ready (for use in React or plain HTML apps)
    

🧠 How the Chatbot Works
------------------------

### 1\. Upload Phase

*   The user uploads a PDF document through the /upload\_pdf/ endpoint.
    
*   The system extracts the raw text using PyPDF2.
    
*   Text is split into overlapping chunks using RecursiveCharacterTextSplitter (from LangChain).
    
*   Each chunk is embedded using HuggingFaceEmbeddings (sentence-transformers/all-mpnet-base-v2).
    
*   FAISS is used to create a vector store from these embeddings.
    
*   A new LangGraph chatbot is created with:
    
    *   A retriever node to fetch top-k similar chunks
        
    *   A generation node powered by **Groq's LLaMA-3.3-70B**
        
    *   Memory tracking using MemorySaver
        
*   A unique session\_id is returned to the client via an **HTTP cookie**.
    

### 2\. Chat Phase

*   User sends queries via /chat endpoint.
    
*   LangGraph uses the session's retriever to fetch relevant chunks from FAISS.
    
*   The context is passed into a custom prompt template.
    
*   LLaMA-3.3-70B generates a response.
    
*   The session maintains memory via MemorySaver.
    

📁 Project Structure
--------------------

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   rag_chatbot_fastapi/  ├── app/  │   ├── main.py             # FastAPI app instance  │   ├── api.py              # Routes for upload_pdf and chat  │   ├── pdf_utils.py        # PDF text extraction logic  │   ├── vector_utils.py     # Text chunking, embedding, FAISS  │   ├── langgraph_flow.py   # LangGraph setup and chatbot creation  ├── uploads/                # Temporary PDF upload folder  ├── requirements.txt        # Python dependencies  ├── README.md               # Project documentation   `

🔑 Tech Stack
-------------

PurposeLibrary/TechAPI FrameworkFastAPIPDF ParsingPyPDF2Text SplittingRecursiveCharacterTextSplitter (LangChain)EmbeddingsHuggingFace Transformers (all-mpnet-base-v2)Vector StoreFAISSLanguage ModelGroq's LLaMA-3.3-70B via LangGraphMemory TrackingLangGraph MemorySaverSession ManagementFastAPI Cookies

🧪 API Endpoints
----------------

### POST /upload\_pdf/

Uploads a PDF document and returns a session ID (stored in cookies):

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   curl -X POST -F "file=@resume.pdf" http://localhost:8000/upload_pdf/   `

### POST /chat

Sends a user question to the chatbot:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   POST /chat  {    "message": "What is the objective of this document?"  }   `

> Note: The session\_id is automatically retrieved from the cookie.

🧹 Auto File Cleanup
--------------------

To ensure user privacy and reduce storage usage, uploaded PDF files are **automatically deleted** right after they are embedded and stored in FAISS.

🛠️ Setup Instructions
----------------------

1.  Clone the repository:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   git clone https://github.com/yourusername/rag_chatbot_fastapi  cd rag_chatbot_fastapi   `

1.  Create a virtual environment:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv venv  source venv/bin/activate  # or venv\Scripts\activate on Windows   `

1.  Install the dependencies:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

1.  Set your Groq API Key:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   export GROQ_API_KEY=your_key_here       # For Linux/macOS  set GROQ_API_KEY=your_key_here          # For Windows CMD   `

1.  Run the server:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   uvicorn main:app --reload   `

1.  Access Swagger UI at:
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   http://127.0.0.1:8000/docs   `

✨ Possible Improvements
-----------------------

*   Build a React-based frontend with file uploader and chat box
    
*   Add file size limits (e.g., 5MB)
    
*   Store FAISS vector index on disk (persistence)
    
*   Add session expiration logic
    
*   Use RAGAS for performance evaluation
    

🙋‍♂️ Author
------------

Built with ❤️ by **Alok**, AI/ML Researcher and Developer.

If you found this helpful, feel free to ⭐ the repo or reach out and connect!