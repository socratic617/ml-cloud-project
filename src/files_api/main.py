"""
Main entry point for the FastAPI application.

This module initializes and configures the FastAPI app,
including setting up routes and managing the S3 bucket name.
"""
import os

from fastapi import FastAPI

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

    return app

if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
