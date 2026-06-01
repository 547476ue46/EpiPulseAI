document.addEventListener("DOMContentLoaded", function () {

  /* ---------------- SEARCH ---------------- */
  const input = document.getElementById("searchInput");
  const cards = document.querySelectorAll(".card");

  input.addEventListener("input", function () {
    const value = input.value.toLowerCase();

    cards.forEach(card => {
      card.style.display =
        card.innerText.toLowerCase().includes(value)
          ? "block"
          : "none";
    });
  });

  /* ---------------- GRAPHS ---------------- */
  new Chart(document.getElementById("chart1"), {
    type: "line",
    data: {
      labels: ["Mon","Tue","Wed","Thu","Fri"],
      datasets: [{
        label: "Usage",
        data: [10,20,15,30,25],
        borderColor: "#7c5cff"
      }]
    }
  });

  new Chart(document.getElementById("chart2"), {
    type: "bar",
    data: {
      labels: ["Speed","AI","UX"],
      datasets: [{
        label: "Score",
        data: [90,85,88],
        backgroundColor: ["#7c5cff","#4cc9f0","#00d4ff"]
      }]
    }
  });

});

/* ---------------- CHAT AI ---------------- */
function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (!text) return;

  const chat = document.getElementById("chatBox");

  // USER
  const user = document.createElement("div");
  user.className = "msg user";
  user.innerText = text;
  chat.appendChild(user);

  // AI
  const ai = document.createElement("div");
  ai.className = "msg ai";
  ai.innerText = "Thinking... 🤖";
  chat.appendChild(ai);

  let msg = text.toLowerCase();
  let reply = "";

  setTimeout(() => {

    if (msg.includes("hello") || msg.includes("hi")) {
      reply = "Hello 👋 I am EpiPulseAI!";
    }
    else if (msg.includes("features")) {
      reply = "I have Chat UI, Dashboard graphs and Search system ⚡";
    }
    else if (msg.includes("dashboard")) {
      reply = "Dashboard shows AI usage analytics 📊";
    }
    else if (msg.includes("help")) {
      reply = "Try: hello, features, dashboard 🙂";
    }
    else {
      reply = "I am a demo AI assistant for your project 🚀";
    }

    ai.innerText = reply;
    chat.scrollTop = chat.scrollHeight;

  }, 700);

  input.value = "";
}