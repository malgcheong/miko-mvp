
### 리턴제로 선택

가격, 성능, 속도 측면에서 비교했을 때, MIKO 프로젝트에서는 리턴제로 서비스가 가장 적합하다고 판단했습니다. 환경은 Apple M1에서 테스트되었습니다.

1. 가격 측면    
**비교: OpenAI Whisper > 리턴제로 > Naver ClovaSpeech**  
기본 10시간 무료 제공하는 리턴제로가 압도적인 우위입니다.  
    - OpenAI Whisper: 라이브러리라서 무료
    - 리턴제로: 모든 유저에게 가입 즉시 기본 10시간을 무료 제공
    - Naver ClovaSpeech: 가입시 20분 무료, 15초에 4원 부과, 10시간에 9600원

2. 성능 측면
**비교: OpenAI Whisper > Naver ClovaSpeech > 리턴제로**  
26초 음성 파일을 STT 변환했을 때, 다음과 같은 에러가 있었습니다.  
    - OpenAI Whisper: 3군데 에러 ([whisper.txt](https://github.com/malgcheong/miko-mvp/blob/9c9f7c9060acd3be40b6ee573c27f9bf3aecfcd4/stt/whisper.txt))
    - Naver ClovaSpeech: 4군데 에러 ([naverclova.txt](https://github.com/malgcheong/miko-mvp/blob/9c9f7c9060acd3be40b6ee573c27f9bf3aecfcd4/stt/naverclova.txt))
    - 리턴제로: 6군데 에러 ([returnzero.txt](https://github.com/malgcheong/miko-mvp/blob/9c9f7c9060acd3be40b6ee573c27f9bf3aecfcd4/stt/returnzero.txt))

3. 속도 측면
**비교: Naver ClovaSpeech > 리턴제로> OpenAI Whisper**  
STT 변환 속도를 비교했을 때, Naver ClovaSpeech가 가장 빠릅니다.  
    - Naver ClovaSpeech: 2.66초
    - 리턴제로: 3.25초
    - OpenAI Whisper: 16분 38.71초