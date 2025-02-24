from tensorflow import keras

def load_model():
    hate_speech_model = keras.models.load_model(r'C:\Users\ShanthoshS\HappyFox\model\hate_speech.keras')
    return hate_speech_model
