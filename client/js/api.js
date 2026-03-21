async function sendToBackend(text) {

    try {

        const response = await fetch("http://127.0.0.1:5000/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        displayResult(data.result);

    } catch (error) {

        console.error("API Error:", error);

        displayResult("Server Error");

    }

}