import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

import json
import requests
import time


client_id = os.getenv("RT_CLIENT_ID")
client_secret = os.getenv("RT_CLIENT_SECRET")

# Measure time for authentication request
start_time = time.time()
resp = requests.post(
    'https://openapi.vito.ai/v1/authenticate',
    data={
        'client_id': client_id,
        'client_secret': client_secret
    }
)
end_time = time.time()
print(f"Authentication request took {end_time - start_time:.2f} seconds")

resp.raise_for_status()
accessToken = resp.json()['access_token']
print(f"Access Token: {accessToken}")

config = {
    "use_diarization": False,
    "use_itn": False,
    "use_disfluency_filter": False,
    "use_profanity_filter": False,
    "use_paragraph_splitter": True,
    "paragraph_splitter": {
        "max": 50
    }
}

# Measure time for transcription request submission
start_time = time.time()
resp = requests.post(
    'https://openapi.vito.ai/v1/transcribe',
    headers={'Authorization': 'bearer ' + accessToken},
    data={'config': json.dumps(config)},
    files={'file': open('miko-mvp/stt/test.m4a', 'rb')}
)
end_time = time.time()
print(f"Transcription request submission took {end_time - start_time:.2f} seconds")

resp.raise_for_status()
transcription_id = resp.json()['id']
print(f"Transcription ID: {transcription_id}")

# Measure total time for transcription processing
processing_start_time = time.time()

# Check the status of the transcription
status_url = f'https://openapi.vito.ai/v1/transcribe/{transcription_id}'
while True:
    start_time = time.time()
    status_resp = requests.get(
        status_url,
        headers={'Authorization': 'bearer ' + accessToken}
    )
    end_time = time.time()
    print(f"Status request took {end_time - start_time:.2f} seconds")

    status_resp.raise_for_status()
    status_data = status_resp.json()
    print(status_data)

    if status_data['status'] == 'completed':
        processing_end_time = time.time()
        print("Transcription completed.")
        print(status_data['results'])
        break
    elif status_data['status'] == 'failed':
        print("Transcription failed.")
        break
    else:
        print("Transcription in progress. Waiting for 0.01 seconds before checking again...")
        time.sleep(0.01)

total_processing_time = processing_end_time - processing_start_time
print(f"Total transcription processing time: {total_processing_time:.2f} seconds")
