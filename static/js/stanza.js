// Get the sidebar, close button, and notation text elements
var sidebar = document.getElementById("sidebar");
var closeButton = document.getElementById("close-button");
var notationText = document.getElementById("notation-text");

// Listen for click events on the document
document.addEventListener("click", function (event) {
  // If the clicked element has a data-notation attribute
  if (event.target.hasAttribute("data-notation")) {
    // Get the data-notation text
    var text = event.target.getAttribute("data-notation");

    // Update the notation text
    notationText.textContent = text;

    // Show the sidebar
    sidebar.style.transform = "translateX(0)";
  }
});

// Add a click event listener to the close button
closeButton.addEventListener("click", function () {
  // Hide the sidebar
  sidebar.style.transform = "translateX(100%)";
});

// Handle toggling line codes
document.addEventListener("DOMContentLoaded", (event) => {
  const toggleLineCodes = document.getElementById("toggleLineCodes");

  if (toggleLineCodes) {
    toggleLineCodes.addEventListener("click", function () {
      console.log("line codes toggled");
      var lineCodes = document.querySelectorAll(".line-code");
      for (var i = 0; i < lineCodes.length; i++) {
        if (this.checked) {
          lineCodes[i].style.display = "inline";
        } else {
          lineCodes[i].style.display = "none";
        }
      }
    });
  }
});

// Handle shortening the line codes
// We shorten the code from 01.01.01 to 1 (that is, the final .01)
document.addEventListener("DOMContentLoaded", (event) => {
  const shortenLineCodes = document.getElementById("toggleLineCodeShortened");

  if (shortenLineCodes) {
    let originalLineCodes = [];

    shortenLineCodes.addEventListener("click", function () {
      const lineCodeLinks = document.querySelectorAll(".line-code a");

      for (let i = 0; i < lineCodeLinks.length; i++) {
        const lineCodeSpan = lineCodeLinks[i].querySelector("span"); // Assuming the line code is in the first span within the link
        if (this.checked) {
          // Save the original line code
          originalLineCodes[i] = lineCodeSpan.textContent;

          // Shorten the line code
          let code = lineCodeSpan.textContent;
          let parts = code.split(".");
          let lastPart = parts[parts.length - 1];
          lineCodeSpan.textContent = parseInt(lastPart);
        } else {
          // Restore the original line code
          if (originalLineCodes.length) {
            lineCodeSpan.textContent = originalLineCodes[i];
          }
        }
      }
    });
  }
});

// Return to top button
window.addEventListener("scroll", function () {
  var returnToTop = document.getElementById("return-to-top");
  var top = document.getElementById("top");
  var distanceFromTop = top.getBoundingClientRect().top;

  // Show the button after the #top anchor is 100px above the viewport
  if (distanceFromTop < -100) {
    returnToTop.classList.remove("opacity-0", "invisible");
    returnToTop.classList.add("opacity-100");
  } else {
    returnToTop.classList.remove("opacity-100");
    returnToTop.classList.add("opacity-0", "invisible");
  }
});
