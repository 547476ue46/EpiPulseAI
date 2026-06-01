document.addEventListener("DOMContentLoaded", function () {

  /* ---------------- SEARCH ---------------- */
  const input = document.getElementById("searchInput");
  const cards = document.querySelectorAll(".card");

  input.addEventListener("input", function () {
    const value = input.value.toLowerCase();

    cards.forEach(card => {
      const text = card.innerText.toLowerCase();

      if (text.includes(value)) {
        card.style.display = "block";
      } else {
        card.style.display = "none";
      }
    });
  });

  /* ---------------- CHART 1 ---------------- */
  new Chart(document.getElementById("chart1"), {
    type: "line",
    data: {
      labels: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
      datasets: [{
        label: "Usage",
        data: [12, 18, 10, 25, 22, 30, 28],
        borderColor: "#7c5cff",
        tension: 0.4
      }]
    }
  });

  /* ---------------- CHART 2 ---------------- */
  new Chart(document.getElementById("chart2"), {
    type: "bar",
    data: {
      labels: ["Speed","AI","UX","Stability"],
      datasets: [{
        label: "Score",
        data: [90, 85, 88, 95],
        backgroundColor: ["#7c5cff","#4cc9f0","#00d4ff","#9b5cff"]
      }]
    }
  });

});