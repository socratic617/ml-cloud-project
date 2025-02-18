"""
    TODO
"""
import os
from datetime import datetime
from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    FastAPI,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from files_api.s3.write_objects import upload_s3_object

#####################
# --- Constants --- #
#####################

# s3_bucket_name = os.environ["some-s3-bucket-lesson-57"]

# Instance of FastAPI
# Labeled "APP" in all caps because it is a constant, defined
#  at the global scope. Using uppercase helps prevent state-related
# bugs and signals to others that it should be treated as a constant.

# app = FastAPI()

####################################
# --- Request/response schemas --- #
####################################

#create/read (CRud)
class PutFileResponse(BaseModel):
    """
        TODO
    """
    file_path: str
    message: str

# read (cRud)
class FileMetadata(BaseModel):
    """
        TODO
    """
    file_path: str
    last_modified: datetime
    size_bytes: int

class GetFilesResponse(BaseModel):
    """
        TODO
    """
    files: list[FileMetadata]
    next_page_token: Optional[str]

class GetFilesQueryParams(BaseModel):
    """
        TODO
    """
    page_size: int = 10
    directory: Optional[str] = ""
    page_token: Optional[str] = None

# delete (cruD)
class DeleteFileResponse(BaseModel):
    """
        TODO
    """
    message: str



##################
# --- Routes --- #
##################
def create_app(s3_bucket_name: str | None = None) -> FastAPI:
    """Create a FastAPI application."""
    print("TESTIE")
    s3_bucket_name = s3_bucket_name or os.environ["S3_BUCKET_NAME"]
    app = FastAPI()

    @app.put("/files/{file_path:path}")
    async def upload_file(file_path: str, file: UploadFile, response: Response) -> PutFileResponse:
        """Upload a file."""

        file_contents: bytes = await file.read()

        object_already_exists_at_path = object_exists_in_s3(s3_bucket_name, object_key=file_path)
        if object_already_exists_at_path:
            message = f"Existing file updated at path: /{file_path}"
            response.status_code = status.HTTP_200_OK
        else:
            message = f"New file uploaded at path: /{file_path}"
            response.status_code = status.HTTP_201_CREATED

        upload_s3_object(
            bucket_name=s3_bucket_name,
            object_key=file_path,
            file_content=file_contents,
            content_type=file.content_type,
        )

        return PutFileResponse(
            file_path=f"{file_path}",
            message=message
        )

    @app.get("/files")
    async def list_files(
        query_params: GetFilesQueryParams = Depends(),  # noqa: B008
    ) -> GetFilesResponse:
        """List files with pagination."""
        if query_params.page_token:
            files, next_page_token = fetch_s3_objects_using_page_token(
                bucket_name=s3_bucket_name,
                continuation_token=query_params.page_token,
                max_keys=query_params.page_size,
            )
        else:
            files, next_page_token = fetch_s3_objects_metadata(
                bucket_name=s3_bucket_name,
                prefix=query_params.directory,
                max_keys=query_params.page_size,
            )

        file_metadata_objs = [
            FileMetadata(
                file_path=f"{item['Key']}",
                last_modified=item["LastModified"],
                size_bytes=item["Size"],
            )
            for item in files
        ]
        return GetFilesResponse(files=file_metadata_objs, next_page_token=next_page_token if next_page_token else None)

    @app.head("/files/{file_path:path}")
    async def get_file_metadata(file_path: str, response: Response) -> Response:
        """Retrieve file metadata.

        Note: by convention, HEAD requests MUST NOT return a body in the response.
        """
        get_object_response = fetch_s3_object(s3_bucket_name, object_key=file_path)
        response.headers["Content-Type"] = get_object_response["ContentType"]
        response.headers["Content-Length"] = str(get_object_response["ContentLength"])
        response.headers["Last-Modified"] = get_object_response["LastModified"].strftime("%a, %d %b %Y %H:%M:%S GMT")
        response.status_code = status.HTTP_200_OK
        return response


    @app.get("/files/{file_path:path}")
    async def get_file(
        file_path: str,
    ) -> StreamingResponse:
        """Retrieve a file."""
        get_object_response = fetch_s3_object(s3_bucket_name, object_key=file_path)
        return StreamingResponse(
            content=get_object_response["Body"],
            media_type=get_object_response["ContentType"],
        )


    @app.delete("/files/{file_path:path}")
    async def delete_file(
        file_path: str,
        response: Response,
    ) -> Response:
        """Delete a file.

        #NOTE: DELETE requests MUST NOT return a body in the response."""
        delete_s3_object(s3_bucket_name, object_key=file_path)
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    return app

if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
