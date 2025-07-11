from fastapi import FastAPI

app = FastAPI()

# Differnt type of endpoints
# GET, POST, PUT, DELETE

# GET: Retrieve data
# POST: Create new data
# PUT: Update existing data
# DELETE: Remove data

# Define a simple root endpoint 
@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Chatbot API!"}

