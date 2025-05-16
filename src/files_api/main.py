"""
Main entry point for the FastAPI application.

This module initializes and configures the FastAPI app,
including setting up routes and managing the S3 bucket name.
"""
import os

from fastapi import FastAPI
import pydantic

from files_api.errors import handle_pydantic_validation_errors
from files_api.routes import ROUTER

from files_api.settings import Settings

##################
# --- Routes --- #
##################
def create_app(settings: Settings | None = None) -> FastAPI:
    """Create a FastAPI application."""
    settings = settings or Settings()
    app = FastAPI()
    app.state.settings = settings


    # adding arbitrary properties to state defining a s3 bucket name on the state obj
    app.include_router(ROUTER)
    app.add_exception_handler(
        exc_class_or_status_code=pydantic.ValidationError,
        handler=handle_pydantic_validation_errors
    )

    return app

if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
