const mic_btn = document.querySelector('#mic');
const playback = document.querySelector('.playback');
let can_record = false;
let is_recording = false;
mic_btn.addEventListener('click', ToggleMic);
let recorder = null;
let formData = new FormData();
let chunks = [];


function SetUpAudio(){
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia)
    {
        navigator.mediaDevices
            .getUserMedia({
                audio: true
            })
            .then(SetUpStream)
            .catch((err) => {
                console.log(err);
            });
    }
}

SetUpAudio();

function SetUpStream(stream){
//    recorder = new MediaRecorder(stream);
    recorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=pcm' });
    recorder.ondataavailable = (e) => {

        chunks.push(e.data);
    };
    recorder.onstop = (e) => {
        const blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
        const audioURL = window.URL.createObjectURL(blob);
        playback.src = audioURL;
        // Append the blob to the FormData object
        formData.append("audio", blob);
        console.log("Recorder for data", formData)
        chunks = [];
    };
    can_record = true;
}

function ToggleMic(){
    if (!can_record) return;
    is_recording = !is_recording;
    if (is_recording) {
        recorder.start();
        mic_btn.classList.add("is-recording");
    } else {
        recorder.stop();
        mic_btn.classList.remove("is-recording");
    }
}

document.getElementById("seek-assistance-btn").addEventListener("click", function() {
    // Send a POST request to the Flask route '/result' with the recorded audio
    fetch("/result", {  // Directly specify the URL here
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Print response from Flask
    })
    .catch(error => {
        console.error("Error:", error);
    });
});