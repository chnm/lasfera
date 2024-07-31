document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".dropdown-toggle").forEach((button) => {
    button.addEventListener("click", function () {
      const dropdown = this.nextElementSibling;
      const isOpen = !dropdown.classList.contains("hidden");
      document
        .querySelectorAll("nav .relative ul")
        .forEach((ul) => ul.classList.add("hidden"));
      document
        .querySelectorAll(".dropdown-toggle")
        .forEach((btn) => btn.classList.remove("dropdown-open"));

      if (!isOpen) {
        dropdown.classList.remove("hidden");
        this.classList.add("dropdown-open");
      }
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest("nav")) {
      document
        .querySelectorAll("nav .relative ul")
        .forEach((ul) => ul.classList.add("hidden"));
      document
        .querySelectorAll(".dropdown-toggle")
        .forEach((btn) => btn.classList.remove("dropdown-open"));
    }
  });
});

/* Hamburger menu navigation */
document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menu-toggle");
  const menu = document.getElementById("menu");

  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      if (menu.classList.contains("menu-hidden")) {
        menu.classList.remove("menu-hidden");
      } else {
        menu.classList.add("menu-hidden");
      }
    });
  }
});
