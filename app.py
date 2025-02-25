from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

# custom module loading statements
from content.main import get_enhanced_content
from content.schema import InputSchema

from model.schema import HateSpeechInputSchema
from model.load_model import load_model

from thread_summarizer.main import summarize_long_thread
from thread_summarizer.schema import InputSummarySchema

from github_crawler.file_extractor import extract_and_combine_code 
from github_crawler.all_links import recursive_crawl
from github_crawler.schema import CodeInputSchema
from github_crawler.main import code_eval, code_eval_test
from github_crawler.utils import text_splitter



hate_text_det_model = load_model()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_content")
async def generate_content(request: InputSchema):
    try:
        input_data = InputSchema(**request.dict())
        result = get_enhanced_content(input_data.input_text, input_data.style)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@app.post("/predict_text")
async def predict_text(request: HateSpeechInputSchema):
    try:
        user_input = tf.constant([request.input_text])
        prediction = hate_text_det_model.predict(user_input)[0]  # Get first prediction

        labels = ["hate_speech", "offensive_speech", "neither"]
        confidence_scores = {label: float(score) for label, score in zip(labels, prediction)}

        max_index = prediction.argmax()
        predicted_label = labels[max_index]
        is_offensive = predicted_label != "neither"

        return {
            "predicted_label": predicted_label,
            "is_offensive": is_offensive,
            "confidence_scores": confidence_scores
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/summary")
async def summary(request : InputSummarySchema):
    try:
        thread_text = request.thread_text
        summary = summarize_long_thread(thread_text=thread_text)
        return { 'summary' : summary}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    
@app.post("/repo_evaluvation")
async def model_repo_eval_endpoint(request: CodeInputSchema):
    try:
        url = request.dict().get("url")
        res = await recursive_crawl(url)
        combined_code = await extract_and_combine_code(res)
        chunk_text = text_splitter.split_text(combined_code)

        # Evaluate the code
        code_evaluvation_res = code_eval_test(chunk_text)
        return code_evaluvation_res

    except json.JSONDecodeError as json_err:
        raise HTTPException(status_code=400, detail=f"JSON Parsing Error: {json_err}")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
     