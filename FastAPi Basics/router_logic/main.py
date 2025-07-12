from fastapi import FastAPI
from greetings import router as greetings_router

# step1: Create a FastAPI instance
app = FastAPI()

# step2: Include the greetings router
app.include_router(greetings_router)


