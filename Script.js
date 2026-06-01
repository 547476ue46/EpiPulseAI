function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();

  if (!text) return;

  const chat = document.getElementById("chatContainer");

  // USER MESSAGE
  const userMsg = document.createElement("div");
  userMsg.className = "msg user";
  userMsg.innerText = text;
  chat.appendChild(userMsg);

  // AI MESSAGE (placeholder)
  const aiMsg = document.createElement("div");
  aiMsg.className = "msg ai";
  aiMsg.innerText = "Thinking... 🤖";
  chat.appendChild(aiMsg);

  // Auto scroll
  chat.scrollTop = chat.scrollHeight;

  // Simple AI responses (demo logic)
  setTimeout(() => {
    let response = "";

    const msg = text.toLowerCase();

    if (msg.includes("hello") || msg.includes("hi")) {
      response = "Hello 👋 How can I help you with EpiPulseAI?";
    }
    else if (msg.includes("what is this")) {
      response = "This is EpiPulseAI — a ChatGPT-style frontend UI project.";
    }
    else if (msg.includes("features")) {
      response = "It includes AI-style UI, chat interface, and dashboard design.";
    }
    else if (msg.includes("help")) {
      response = "Try asking: features, about, or hello 🙂";
    }
    else {
      response = "I am a demo AI inside EpiPulseAI. You can expand my logic anytime 🚀";
    }

    aiMsg.innerText = response;

    chat.scrollTop = chat.scrollHeight;

  }, 800);

  input.value = "";
}

// OPTIONAL: press Enter to send message
document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("userInput");

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});