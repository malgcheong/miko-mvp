from transformers import pipeline
import torch

# GPU가 사용 가능하면 GPU를 사용합니다.
device = 0 if torch.cuda.is_available() else -1
if device == 0:
    print("Using GPU")
else:
    print("Using CPU")
    
# Whisper 모델과 파이프라인을 설정합니다.
pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v2",
    chunk_length_s=30,  # 청크 길이를 조절할 수 있습니다.
    device=device,
    return_timestamps=True
)

# 오디오 파일 경로를 설정합니다.
audio_path = "../test.m4a"

# 음성을 텍스트와 타임스탬프로 변환합니다.
result = pipe(audio_path)

# 결과를 출력합니다.
for chunk in result["chunks"]:
    print(f"Text: {chunk['text']}, Start: {chunk['timestamp'][0]}, End: {chunk['timestamp'][1]}")
