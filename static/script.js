const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", () => {
    const message = userInput.value.trim();
    if(message === "") return;

    appendMessage("You", message);
    userInput.value = "";

    fetch("/get_response", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    })
    .then(response => response.json())
    .then(data => appendMessage("Bot", data.response));
});

function appendMessage(sender, message){
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message");
    msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
