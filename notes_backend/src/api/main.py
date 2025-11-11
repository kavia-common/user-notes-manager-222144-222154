from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.notes import router as notes_router

openapi_tags = [
    {
        "name": "Health",
        "description": "Service health and operational endpoints.",
    },
    {
        "name": "Notes",
        "description": "CRUD operations for managing notes.",
    },
]

app = FastAPI(
    title="Notes Backend API",
    description="A simple FastAPI application exposing CRUD endpoints for notes.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to trusted origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Returns a simple health status message.",
)
def health_check():
    """Return service health status.

    Returns:
        dict: A simple message indicating the service is healthy.
    """
    return {"message": "Healthy"}


# Register routes
app.include_router(notes_router)
