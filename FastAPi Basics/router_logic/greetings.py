from fastapi import APIRouter, HTTPException, UploadFile, File

# Step 1: Create a new APIRouter instance
router = APIRouter()

# Step 2: Define a simple root endpoint
@router.get("/hello")
def say_hello():
    return {"message": "Hello, World!"} 

@router.get("/greet/{name}")    
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}   


