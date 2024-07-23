let localStream;
let isMuted = false;
let isCameraOff = false;

// Function to start the camera stream using a specific device ID
async function startCamera(deviceId) {
    try {
        // Stop any existing tracks
        if (localStream) {
            localStream.getTracks().forEach(track => track.stop());
        }

        // Request the camera stream with the specific device ID
        localStream = await navigator.mediaDevices.getUserMedia({ 
            video: { deviceId: deviceId ? { exact: deviceId } : undefined },
            audio: true
        });
        
        // Get the video element
        const videoElement = document.getElementById('myCamera');
        
        // Set the source of the video element to the stream
        videoElement.srcObject = localStream;

        updateButtons();
    } catch (error) {
        console.error('Error accessing camera:', error);
    }
}

// Function to list all video input devices (cameras)
async function listCameras() {
    try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoInputDevices = devices.filter(device => device.kind === 'videoinput');
        
        const cameraSelect = document.getElementById('cameraSelect');
        cameraSelect.innerHTML = '';

        videoInputDevices.forEach((device, index) => {
            const option = document.createElement('option');
            option.value = device.deviceId;
            option.text = device.label || `Camera ${index + 1}`;
            cameraSelect.appendChild(option);
        });

        cameraSelect.addEventListener('change', () => {
            startCamera(cameraSelect.value);
        });

        if (videoInputDevices.length > 0) {
            startCamera(videoInputDevices[0].deviceId);
        }
    } catch (error) {
        console.error('Error listing cameras:', error);
    }
}

// Function to toggle mute
function toggleMute() {
    if (localStream) {
        localStream.getAudioTracks().forEach(track => {
            track.enabled = !track.enabled;
        });
        isMuted = !isMuted;
        updateButtons();
    }
}

// Function to toggle camera
function toggleCamera() {
    if (localStream) {
        localStream.getVideoTracks().forEach(track => {
            track.enabled = !track.enabled;
        });
        isCameraOff = !isCameraOff;
        updateButtons();
    }
}

// Function to update button text
function updateButtons() {
    const muteButton = document.getElementById('muteButton');
    const cameraButton = document.getElementById('cameraButton');

    muteButton.textContent = isMuted ? 'Unmute' : 'Mute';
    cameraButton.textContent = isCameraOff ? 'Turn Camera On' : 'Turn Camera Off';
}

// Start listing cameras when the page loads
window.addEventListener('load', listCameras);

// Add event listeners for buttons
document.getElementById('muteButton').addEventListener('click', toggleMute);
document.getElementById('cameraButton').addEventListener('click', toggleCamera);
