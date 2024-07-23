import time
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import librosa
from pydub import AudioSegment

# 모델과 프로세서를 로드합니다.
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3")

# 오디오 파일을 청크로 나누는 함수
def split_audio(file_path, chunk_length_ms=30000):
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

# 각 청크를 처리하는 함수
def transcribe_chunk(chunk, sample_rate=16000):
    chunk.export("temp.wav", format="wav")
    audio, sr = librosa.load("temp.wav", sr=sample_rate)
    input_features = processor(audio, sampling_rate=sr, return_tensors="pt").input_features

    with torch.no_grad():
        predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    return transcription[0]

# 메인 함수
def transcribe_long_audio(file_path):
    chunks = split_audio(file_path)
    full_transcription = ""
    start_time = time.time()  # 변환 작업 시작 시간 기록
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")
        transcription = transcribe_chunk(chunk)
        full_transcription += transcription + " "
    end_time = time.time()  # 변환 작업 끝 시간 기록
    print(f"Total transcription time: {end_time - start_time:.2f} seconds")  # 소요 시간 출력
    return full_transcription.strip()

# 긴 오디오 파일을 처리합니다.
audio_path = "miko-mvp/stt/test.m4a"  # 실제 음성 파일 경로
full_transcription = transcribe_long_audio(audio_path)
print(full_transcription)
