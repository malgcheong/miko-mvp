let mediaRecorder;
let socket;
let chunks = [];

document.getElementById("startButton").addEventListener("click", async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            chunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        chunks = [];
        socket.emit('audio', blob);
    };

    mediaRecorder.start();

    socket = io.connect('http://localhost:5001');  // 서버의 URL로 연결
    socket.on('transcription', (data) => {
        document.getElementById("transcription").innerText += data.text + ' ';
    });
});

// 특정 시점에 requestData() 호출
document.getElementById("requestDataBtn").addEventListener("click", () => {
    mediaRecorder.requestData();
    const blob = new Blob(chunks, { type: 'audio/webm' });
    console.log(chunks)
    socket.emit('audio', blob);
    chunks = [];
  });

document.getElementById("stopButton").addEventListener("click", () => {
    mediaRecorder.stop();
});
