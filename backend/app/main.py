from fastapi import FastAPI, UploadFile, File, HTTPException
from app.schema.input import CodeFileInput
from app.services import parsing
import os
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload endpoint to receive code file, validate it, and prepare for narration.
    """
    filename = file.filename
    contents = await file.read()

    try:
        model = CodeFileInput(
            file_name=filename,
            file_type=os.path.splitext(filename)[-1][1:],
            file_content=contents.decode("utf-8")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")

    structure = parsing.extract_ast_metadata(model.file_content)

    return {
        "message": "File accepted",
        "type": model.file_type,
        "structure": structure
    }