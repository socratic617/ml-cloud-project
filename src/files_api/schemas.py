####################################
# --- Request/response schemas --- #
####################################
from datetime import datetime
from typing import (
    List,
    Optional,
)
from unittest.mock import DEFAULT

from pydantic import (
    BaseModel,
    Field,
)

DEFAULT_GET_FILES_PAGE_SIZE = 10
DEFAULT_GET_FILES_MIN_PAGE_SIZE = 10
DEFAULT_GET_FILES_MAX_PAGE_SIZE = 100
DEFAULT_GET_FILES_DIRECTORY = ""

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
    files: List[FileMetadata]
    next_page_token: Optional[str]

class GetFilesQueryParams(BaseModel):
    """
        TODO
    """
    page_size: int = Field(
        DEFAULT_GET_FILES_PAGE_SIZE,
        ge=DEFAULT_GET_FILES_MIN_PAGE_SIZE,
        le=DEFAULT_GET_FILES_MAX_PAGE_SIZE,
    )
    directory: Optional[str] = ""
    page_token: Optional[str] = None

# delete (cruD)
class DeleteFileResponse(BaseModel):
    """
        TODO
    """
    message: str
