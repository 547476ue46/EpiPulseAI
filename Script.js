document.addEventListener("DOMContentLoaded", function () {

  /* ---------------- SEARCH ---------------- */
  const input = document.getElementById("searchInput");
  const cards = document.querySelectorAll(".card");

  input.addEventListener("input", function () {
    const value = input.value.toLowerCase();

    cards.forEach(card => {
      const text = card.innerText.toLowerCase();
      card.style.display = text.includes(value) ? "block" : "none";
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

/* ---------------- CHAT ---------------- */
function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (!text) return;

  const chat = document.getElementById("chatBox");

  // user msg
  const user = document.createElement("div");
  user.className = "msg user";
  user.innerText = text;
  chat.appendChild(user);

  // ai msg
  const ai = document.createElement("div");
  ai.className = "msg ai";
  ai.innerText = "Thinking... 🤖";
  chat.appendChild(ai);

  setTimeout(() => {
    ai.innerText = "This is a demo AI response from EpiPulseAI 🚀";
  }, 700);

  input.value = "";
  chat.scrollTop = chat.scrollHeight;
}