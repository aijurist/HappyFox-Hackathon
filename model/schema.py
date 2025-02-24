from pydantic import BaseModel, Field

class HateSpeechInputSchema(BaseModel):
    input_text: str = Field(description="Input text to verify for the hate speech")