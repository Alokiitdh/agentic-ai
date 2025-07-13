import os, uuid
from fastapi import APIRouter, HTTPException, UploadFile, File
from pdf_utils import extract_text_from_pdf
from vector_utils import chunk_and_embed_text, store_vectorstore
from langgraph_flow import create_langgraph_chatbot, chatbot_sessions
from fastapi.responses import JSONResponse
from fastapi import Request

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Ensure uploads and db folders exist
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Construct full path safely
    filename = f"{session_id}_{file.filename}"
    file_location = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_location)
        if not text:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")

        # Process vector store
        chunks = chunk_and_embed_text(text)
        store_vectorstore(session_id, chunks)

        # Create chatbot
        create_langgraph_chatbot(session_id, chunks)

        # set session id as cookie
        response = JSONResponse(
                    content={"message": "PDF uploaded and processed successfully",
                            "session_id": session_id}
        )
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    finally:
        # Clean up the uploaded file
        if os.path.exists(file_location):
            os.remove(file_location)


@router.post("/chat")
async def chat(request: Request, message: str):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Invalid or missing session ID")
    
    chatbot = chatbot_sessions[session_id]

    result = chatbot.invoke({"question": message},
                            config={"configurable": {"thread_id": f"{session_id}-thread"}}
    )
    return {"answer": result["answer"]}
