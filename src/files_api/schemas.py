####################################
# --- Request/response schemas --- #
####################################
from datetime import datetime
from typing import (
    List,
    Optional,
)
from typing_extensions import Self
from unittest.mock import DEFAULT

from pydantic import (
    BaseModel,
    Field,
    model_validator
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
    directory: Optional[str] = DEFAULT_GET_FILES_DIRECTORY
    page_token: Optional[str] = None

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.page_token:
            get_files_query_params: dict = self.model_dump(exclude_unset=True)
            page_size_set = "page_size" in get_files_query_params.keys()
            directory_set = "directory" in get_files_query_params.keys()
            if page_size_set or directory_set:
                raise ValueError("page_token is mutually exclusive with page_size and directory")
        return self

# delete (cruD)
class DeleteFileResponse(BaseModel):
    """
        TODO
    """
    message: str
