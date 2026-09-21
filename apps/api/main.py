"""TerraSeek FastAPI Application."""

from contextlib import asynccontextmanager
import logging
import time
import uuid
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from terraseek.config import settings
from terraseek.db.session import init_db
from terraseek.schemas.common import APIErrorResponse, APIErrorDetails

from apps.api.routes import (
    health,
    search,
    retrieval,
    sites,
    change,
    temporal,
    evidence,
    review,
    jobs,
    reports,
    ingestion,
)

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
)
logger = logging.getLogger("terraseek.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting TerraSeek API...")
    init_db()
    yield
    logger.info("Shutting down TerraSeek API...")


app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
    description="TerraSeek: Satellite-imagery search and change-analysis platform. Truth-in-AI Remote Sensing Intelligence.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000.0
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-MS"] = f"{process_time:.2f}"
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request payload or query parameters.",
                "request_id": req_id,
                "details": {"errors": exc.errors()},
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    logger.exception(f"Unhandled server error [request_id={req_id}]: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred processing your satellite intelligence request.",
                "request_id": req_id,
                "details": {"error_type": type(exc).__name__},
            }
        },
    )


# Mount API routes under /api/v1
api_v1 = "/api/v1"
app.include_router(health.router, prefix=api_v1)
app.include_router(search.router, prefix=api_v1)
app.include_router(retrieval.router, prefix=api_v1)
app.include_router(sites.router, prefix=api_v1)
app.include_router(change.router, prefix=api_v1)
app.include_router(temporal.router, prefix=api_v1)
app.include_router(evidence.router, prefix=api_v1)
app.include_router(review.router, prefix=api_v1)
app.include_router(jobs.router, prefix=api_v1)
app.include_router(reports.router, prefix=api_v1)
app.include_router(ingestion.router, prefix=api_v1)
