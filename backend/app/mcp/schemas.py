from pydantic import BaseModel
from typing import List


class RepositoryRequest(BaseModel):
    path: str


class RepositoryResponse(BaseModel):
    total_files: int
    languages: List[str]
    important_files: List[str]
    files: List[str]