const socket = io();

const videoElement = document.getElementById('video');
const startButton = document.getElementById('start-btn');
const stopButton = document.getElementById('stop-btn');

startButton.addEventListener('click', () => {
    socket.emit('start_video');
});

stopButton.addEventListener('click', () => {
    socket.emit('stop_video');
});

socket.on('start_stream', () => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                videoElement.srcObject = stream;
            })
            .catch(err => {
                console.error("Error accessing camera:", err);
            });
    }
});

socket.on('stop_stream', () => {
    if (videoElement.srcObject) {
        videoElement.srcObject.getTracks().forEach(track => track.stop());
        videoElement.srcObject = null;
    }
});
