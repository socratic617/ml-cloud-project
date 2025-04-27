"""
    ROUTES:

    This module defines the routes for interacting with files stored in an S3 bucket.

    Routes include:
    - Uploading files (`PUT /files/{file_path:path}`)
    - Listing files with pagination (`GET /files`)
    - Retrieving file metadata (`HEAD /files/{file_path:path}`)
    - Downloading files (`GET /files/{file_path:path}`)
    - Deleting files (`DELETE /files/{file_path:path}`)

    Each route interacts with the S3 bucket specified in the application state
    (`app.state.s3_bucket_name`) -> [now currently: `app.state.settings.s3_bucket_name`], using helper functions from the `files_api.s3`
    module for file management.

    All responses are structured based on defined Pydantic models for consistency and ease of use.
"""
from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import StreamingResponse

from files_api.s3.delete_objects import delete_s3_object
from files_api.s3.read_objects import (
    fetch_s3_object,
    fetch_s3_objects_metadata,
    fetch_s3_objects_using_page_token,
    object_exists_in_s3,
)
from files_api.s3.write_objects import upload_s3_object
from files_api.schemas import (
    FileMetadata,
    GetFilesQueryParams,
    GetFilesResponse,
    PutFileResponse,
)
from files_api.settings import Settings

ROUTER = APIRouter()

# ROUTER WORKS like FastAPI Routes
@ROUTER.put("/files/{file_path:path}")
async def upload_file(request: Request,
                      file_path: str,
                      file: UploadFile,
                      response: Response
                      ) -> PutFileResponse:
    """
    Uploads a file to the specified S3 bucket. If the file already
    exists, it is updated; otherwise, a new file is created.

    Returns a response indicating the status of the upload.
    """
    settings: Settings = request.app.state.settings

    file_contents: bytes = await file.read()

    object_already_exists_at_path = object_exists_in_s3(settings.s3_bucket_name, object_key=file_path)
    if object_already_exists_at_path:
        message = f"Existing file updated at path: /{file_path}"
        response.status_code = status.HTTP_200_OK
    else:
        message = f"New file uploaded at path: /{file_path}"
        response.status_code = status.HTTP_201_CREATED

    upload_s3_object(
        bucket_name=settings.s3_bucket_name,
        object_key=file_path,
        file_content=file_contents,
        content_type=file.content_type,
    )

    return PutFileResponse(
        file_path=f"{file_path}",
        message=message
    )

@ROUTER.get("/files")
async def list_files(
    request: Request,
    query_params: GetFilesQueryParams = Depends(),  # noqa: B008
) -> GetFilesResponse:
    """
    List files with pagination.
    """
    settings: Settings = request.app.state.settings

    if query_params.page_token:
        files, next_page_token = fetch_s3_objects_using_page_token(
            bucket_name=settings.s3_bucket_name,
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

@ROUTER.head("/files/{file_path:path}")
async def get_file_metadata(request: Request,
                            file_path: str,
                            response: Response
                            ) -> Response:
    """
    Retrieve file metadata.

    Note: by convention, HEAD requests MUST NOT return a body in the response.
    """
    settings: Settings = request.app.state.settings
    get_object_response = fetch_s3_object(settings.s3_bucket_name, object_key=file_path)
    response.headers["Content-Type"] = get_object_response["ContentType"]
    response.headers["Content-Length"] = str(get_object_response["ContentLength"])
    response.headers["Last-Modified"] = get_object_response["LastModified"].strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.status_code = status.HTTP_200_OK
    return response


@ROUTER.get("/files/{file_path:path}")
async def get_file(
    request: Request,
    file_path: str,
) -> StreamingResponse:
    """
    Retrieve a file.
    """
    #Bussiness Logic:
        # Error Case: Object does not exist in  bucket
        # Error Case: Invalid inputs

    # Internal Server Error:
        # Error Case: Not authenticated/authorized to access object to make calls to AWS
        # Error Case: Access to AWS but non-existent bucket
    settings: Settings = request.app.state.settings
    get_object_response = fetch_s3_object(settings.s3_bucket_name, object_key=file_path)
    return StreamingResponse(
        content=get_object_response["Body"],
        media_type=get_object_response["ContentType"],
    )


@ROUTER.delete("/files/{file_path:path}")
async def delete_file(
    request: Request,
    file_path: str,
    response: Response,
) -> Response:
    """
    Delete a file.
    NOTE: DELETE requests MUST NOT return a body in the response.
    """

    print("app state: ", request.app.state)
    settings: Settings = request.app.state.settings
    delete_s3_object(settings.s3_bucket_name, object_key=file_path)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
