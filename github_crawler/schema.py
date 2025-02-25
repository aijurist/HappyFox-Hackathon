from pydantic import BaseModel, Field
from typing import List, Dict


class LinkSchema(BaseModel):
    links: List[str] = Field(description="List of all links of files and folders.")
    file_links: List[str] = Field(description="List of GitHub links pointing to individual code files inside a repository. These links follow the pattern: 'https://github.com/{username}/{repo}/blob/{branch}/{file_path}'.")
    folder_links: List[str] = Field(description="List of GitHub links pointing to directories or subdirectories inside a repository. These links follow the pattern: 'https://github.com/{username}/{repo}/tree/{branch}/{folder_path}'.")