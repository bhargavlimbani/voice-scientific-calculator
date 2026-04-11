function displayResult(result) {
    document.getElementById("result").innerText = result;

    // Speak result
    const speech = new SpeechSynthesisUtterance("The result is " + result);
    window.speechSynthesis.speak(speech);
}
function append(value) {
    const input = document.getElementById("inputBox");
    input.value += value;
}

function clearInput() {
    document.getElementById("inputBox").value = "";
}

function calculateInput() {
    const text = document.getElementById("inputBox").value;
    sendToBackend(text);
}

function displayResult(result) {

    const input = document.getElementById("inputBox").value;

    document.getElementById("result").innerText = result;

    // 🎤 Speak
    const speech = new SpeechSynthesisUtterance("The result is " + result);
    window.speechSynthesis.speak(speech);

   
    saveHistory(input, result);
}

function saveHistory(input, result) {

    let history = JSON.parse(localStorage.getItem("calcHistory")) || [];

    history.unshift({ input, result });

    // keep only last 10
    if (history.length > 10) history.pop();

    localStorage.setItem("calcHistory", JSON.stringify(history));

    renderHistory();
}

function renderHistory() {

    let history = JSON.parse(localStorage.getItem("calcHistory")) || [];

    let historyDiv = document.getElementById("history");
    historyDiv.innerHTML = "";

    history.forEach(item => {
        let p = document.createElement("p");
        p.innerText = item.input + " = " + item.result;
        historyDiv.appendChild(p);
    });
}
window.onload = function() {
    renderHistory();
};

function clearHistory() {
    localStorage.removeItem("calcHistory");
    renderHistory();
}