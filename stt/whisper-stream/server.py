from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from transformers import pipeline
import torch
import io
from pydub import AudioSegment
import os
import tempfile
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# GPU가 사용 가능한지 확인
device = 0 if torch.cuda.is_available() else -1

# Whisper 모델과 파이프라인 설정
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v2",
    chunk_length_s=30,
    device=device,
    return_timestamps=True
)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio')
def handle_audio(data):
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(data), format="webm")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            audio_segment.export(temp_audio.name, format="wav")
            result = pipe(temp_audio.name)
        os.remove(temp_audio.name)
        
        transcription = ""
        for chunk in result["chunks"]:
            transcription += f"Text: {chunk['text']}, Start: {chunk['timestamp'][0]}, End: {chunk['timestamp'][1]}\n"

        emit('transcription', {'text': transcription})
    except Exception as e:
        print(f"Error processing audio file: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
