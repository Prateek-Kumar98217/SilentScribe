from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import authentication, project, codefile
from app.core.database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(project.router)
app.include_router(codefile.router)