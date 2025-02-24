from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf

# custom module loading statements
from content.main import get_enhanced_content
from content.schema import InputSchema

from model.schema import HateSpeechInputSchema
from model.load_model import load_model

hate_text_det_model = load_model()
app = FastAPI()
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

        # Convert numpy.float32 to Python float
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
