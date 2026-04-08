const micBtn = document.getElementById("micBtn");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-US";

micBtn.addEventListener("click", () => {
    recognition.start();
});

recognition.onresult = function(event) {

    const transcript = event.results[0][0].transcript;

    document.getElementById("voiceText").innerText = transcript;

    document.getElementById("inputBox").value = transcript;

    console.log("Sending:", transcript);

    sendToBackend(transcript);
};