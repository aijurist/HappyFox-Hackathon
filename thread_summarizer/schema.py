from pydantic import BaseModel, Field
from typing import List

class InputSummarySchema(BaseModel):
    thread_text: str = Field(description="Entire conversation history/thread of the form")
    
    
class SummarySchema(BaseModel):
    summary: str = Field(description="Summary of the forum thread.")
