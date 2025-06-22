from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import input

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"message": "Welcome to the SilentScribe!"}

app.include_router(input.router)