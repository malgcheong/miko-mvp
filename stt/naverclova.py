import requests
import json
import time
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = os.getenv("CLOVA_URL")
    # Clova Speech secret key
    secret = os.getenv("CLOVA_SECRET")

    def req_url(self, url, completion, callback=None, userdata=None, forbiddens=None, boostings=None, wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'url': url,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }

        start_time = time.time()
        response = requests.post(headers=headers,
                                 url=self.invoke_url + '/recognizer/url',
                                 data=json.dumps(request_body).encode('UTF-8'))
        end_time = time.time()

        print(f"Request to /recognizer/url took {end_time - start_time:.2f} seconds")
        return response

    def req_object_storage(self, data_key, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                           wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'dataKey': data_key,
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'Content-Type': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }

        start_time = time.time()
        response = requests.post(headers=headers,
                                 url=self.invoke_url + '/recognizer/object-storage',
                                 data=json.dumps(request_body).encode('UTF-8'))
        end_time = time.time()

        print(f"Request to /recognizer/object-storage took {end_time - start_time:.2f} seconds")
        return response

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }

        start_time = time.time()
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        end_time = time.time()

        print(f"Request to /recognizer/upload took {end_time - start_time:.2f} seconds")
        return response

if __name__ == '__main__':
    start_time = time.time()  # 전체 변환 작업 시작 시간 기록
    # res = ClovaSpeechClient().req_url(url='http://example.com/media.mp3', completion='sync')
    # res = ClovaSpeechClient().req_object_storage(data_key='data/media.mp3', completion='sync')
    res = ClovaSpeechClient().req_upload(file='miko-mvp/stt/test.m4a', completion='sync')
    end_time = time.time()  # 전체 변환 작업 끝 시간 기록

    print(res.text)
    print(f"Total transcription time: {end_time - start_time:.2f} seconds")  # 총 소요 시간 출력
