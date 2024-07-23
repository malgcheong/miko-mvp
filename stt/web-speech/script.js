document.addEventListener('DOMContentLoaded', function () {
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const result = document.getElementById('result');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'ko-KR';  // 한국어 설정

    let audioContext;
    let analyser;
    let microphone;
    let audioWorkletNode;
    let isRecognizing = false;
    let finalTranscript = '';

    async function startAudioContext(stream) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        await audioContext.audioWorklet.addModule('audio-processor.js');
        
        microphone = audioContext.createMediaStreamSource(stream);
        audioWorkletNode = new AudioWorkletNode(audioContext, 'volume-processor');
        
        audioWorkletNode.port.onmessage = (event) => {
            const volume = event.data;
            if (volume > 0.03) { // 임계값 설정
                if (!isRecognizing) {
                    recognition.start();
                    isRecognizing = true;
                    startButton.disabled = true;
                    stopButton.disabled = false;
                }
            } else {
                if (isRecognizing) {
                    recognition.stop();
                    isRecognizing = false;
                    startButton.disabled = false;
                    stopButton.disabled = true;
                }
            }
        };

        microphone.connect(audioWorkletNode);
        audioWorkletNode.connect(audioContext.destination);
    }

    recognition.onresult = function (event) {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }
        result.innerHTML = finalTranscript + '<i>' + interimTranscript + '</i>';
    };

    recognition.onerror = function (event) {
        console.error('Speech recognition error', event.error);
        isRecognizing = false;
        startButton.disabled = false;
        stopButton.disabled = true;
    };

    recognition.onend = function () {
        isRecognizing = false;
        startButton.disabled = false;
        stopButton.disabled = true;
    };

    startButton.addEventListener('click', () => {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            startAudioContext(stream);
            result.textContent = '듣는 중...';
        }).catch(err => {
            console.error('Error accessing microphone', err);
        });
    });

    stopButton.addEventListener('click', () => {
        if (isRecognizing) {
            recognition.stop();
            isRecognizing = false;
        }
        if (audioContext) {
            audioContext.close();
        }
        startButton.disabled = false;
        stopButton.disabled = true;
    });
});
