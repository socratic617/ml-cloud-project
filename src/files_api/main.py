"""
Main entry point for the FastAPI application.

This module initializes and configures the FastAPI app,
including setting up routes and managing the S3 bucket name.
"""
import os

from fastapi import FastAPI

from files_api.routes import ROUTER

##################
# --- Routes --- #
##################
def create_app(s3_bucket_name: str | None = None) -> FastAPI:
    """Create a FastAPI application."""
    s3_bucket_name = s3_bucket_name or os.environ["S3_BUCKET_NAME"]
    app = FastAPI()


    # adding arbitrary properties to state defining a s3 bucket name on the state obj
    app.state.s3_bucket_name = s3_bucket_name
    app.include_router(ROUTER)

    return app

if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
