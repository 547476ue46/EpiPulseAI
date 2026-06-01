document.addEventListener("DOMContentLoaded", function () {

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

});