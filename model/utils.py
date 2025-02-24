from tensorflow import keras
import tensorflow as tf
from model.load_model import load_model

speech_classification_model = load_model()
def preprocess_text(input_text):
    try:
        processed_text = tf.constant([input_text])
        return processed_text
    except Exception:
        raise ValueError("Could not preprocess")
    
    
def speech_prediction(input_text):
    try:
        preprocess_text = tf.constant([input_text])
        res = speech_classification_model.predict(preprocess_text)
        return res.tolist()
    except Exception as e:
        raise ValueError("Could not predict the output", e)
    
def speech_classification(input_text):
    try:
        user_input = tf.constant([input_text])
        prediction = speech_classification_model.predict(user_input)[0]  # Get first prediction

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
        raise Exception("Some error in prediction", detail=str(e))