from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.v1.router import api_router as v1_api_router
from src.api.utils.exception_handlers import register_exception_handlers
from src.config import settings
from src.logger import logger, setup_logging
from src.utils.response import Response, Status

load_dotenv(override=True)


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        servers=[
            {
                "url": "http://127.0.0.1:8000",
                "description": "Local Development Server",
            },
        ],
        summary="AI Service API",
        description="AI Service API",
        version="0.1.0",
    )

    setup_logging()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(v1_api_router, prefix="/ai-service/v1")
    register_exception_handlers(app)

    return app


# ========== FAST API APPLICATION ==========
app: FastAPI = create_app()


# ========== HEALTH CHECK ROUTE ==========
@app.get("/health")
def health_check():
    logger.info("Server is Healthy")
    return Response.success(message="Server is Healthy", status_code=Status.OK)
