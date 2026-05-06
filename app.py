import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

import database
import models
from routers import auth, predict, chat, main as main_router

# Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET_KEY", "fallback-secret-key-for-dev")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers
app.include_router(main_router.router)
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(chat.router)

def main():
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=8001, reload=True)

if __name__ == "__main__":
    main()