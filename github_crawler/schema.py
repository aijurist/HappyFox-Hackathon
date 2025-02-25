from pydantic import BaseModel, Field
from typing import List, Dict


class LinkSchema(BaseModel):
    links: List[str] = Field(description="List of all links of files and folders.")
    file_links: List[str] = Field(description="List of GitHub links pointing to individual code files inside a repository. These links follow the pattern: 'https://github.com/{username}/{repo}/blob/{branch}/{file_path}'.")
    folder_links: List[str] = Field(description="List of GitHub links pointing to directories or subdirectories inside a repository. These links follow the pattern: 'https://github.com/{username}/{repo}/tree/{branch}/{folder_path}'.")

class LocationSchema(BaseModel):
    start_line: int = Field(description="The starting line number of the issue in the code.")
    end_line: int = Field(description="The ending line number of the issue in the code.")

class IssueSchema(BaseModel):
    id: int = Field(description="A unique identifier for the issue.")
    title: str = Field(description="A concise explanation of the issue (~4 lines).")
    description: str = Field(description="Detailed explanation and reasoning behind the issue.")
    location: LocationSchema = Field(description="The location of the issue in the code.")

class CodeEvalSchema(BaseModel):
    optimization: List[IssueSchema] = Field(description="List of code optimization suggestions with detailed context.")
    vulnerability: List[IssueSchema] = Field(description="List of identified vulnerabilities with descriptions and locations.")

class CodeInputSchema(BaseModel):
    url: str = Field(description="Github Repository URL to analyse")
