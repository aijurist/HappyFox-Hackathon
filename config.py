from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import os

# loading the environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
llm = GoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=GEMINI_API_KEY)