from fastapi import FastAPI
from db.init_db import init_db
from db.session import SessionLocal, engine
from app.api.v1.router import auth, user, file
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.auth_middleware import AuthMiddleware
from middlewares.cors_middleware import add_cors_middleware
from middlewares.error_handling_middleware import ErrorHandlingMiddleware

from fastapi import FastAPI

app = FastAPI(
    title="File Uploader API",
    description="This application provides a backend solution for uploading, managing, and sharing files, as well as managing users. It offers endpoints for user registration, authentication, user profile management, file upload, listing user files, listing all files (admin only), file analytics, file sharing, updating files, and deleting files.",
    version="1.0.0"
)

@app.get("/")
async def home():
    return {"message": "Welcome to the File Uploader API. Please go to /docs for documentation."}



# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(file.router, prefix="/file", tags=["file"])


# middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware, excluded_paths=["/", "/docs", "/openapi.json", "/auth/token", "/auth/register/"])
add_cors_middleware(app)
app.add_middleware(ErrorHandlingMiddleware)




# Initialize database
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    init_db(db)
    db.close()
