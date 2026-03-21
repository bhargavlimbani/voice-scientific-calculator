function displayResult(result) {
    document.getElementById("result").innerText = result;

    // Speak result
    const speech = new SpeechSynthesisUtterance("The result is " + result);
    window.speechSynthesis.speak(speech);
}