from pydantic import BaseModel, Field
from typing import List, Dict

class InputSchema(BaseModel):
    input_text: str = Field(description="Text which is to be enhanced")
    style: str = Field(description="Style which the user wants the text to be enhanced to")

class Choice(BaseModel):
    id: int = Field(description="The choice ID of the generated text information in a different version")
    text: str = Field(description="The choice text of the generated text information in a different version")
    confidence: float = Field(description="The confidence score of the choice")

class Response(BaseModel):
    choices: List[Choice] = Field(description="Given choices as a list of choices", max_length=3)

class OutputSchema(BaseModel):
    given_text: str = Field(description="The given text to generate the choices")
    response: Response = Field(description="Response to the user containing the generated Choices as a list")