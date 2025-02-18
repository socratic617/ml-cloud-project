####################################
# --- Request/response schemas --- #
####################################
from datetime import datetime
from typing import (
    List,
    Optional,
)

from pydantic import BaseModel

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
    page_size: int = 10
    directory: Optional[str] = ""
    page_token: Optional[str] = None

# delete (cruD)
class DeleteFileResponse(BaseModel):
    """
        TODO
    """
    message: str
