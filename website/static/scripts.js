/* ---menu--- */

const menu = document.querySelector(".menu");
const openMenuBtn = document.querySelector(".open-menu-btn");
const closeMenuBtn = document.querySelector(".close-menu-btn");

[openMenuBtn, closeMenuBtn].forEach((btn) => {
    btn.addEventListener("click", () => {
        menu.classList.toggle("open");
        menu.style.transition = "transform 0.5s ease";
    });
});

menu.addEventListener("transitionend", function() {
    this.removeAttribute("style");
});

menu.querySelectorAll(".dropdown > i").forEach((arrow) => {
    arrow.addEventListener("click", function() {
        this.closest(".dropdown").classList.toggle("active");
    });
});

// Function to toggle password visibility
function togglePasswordVisibility(toggleButtonId, passwordFieldId) {
    const toggleButton = document.querySelector(toggleButtonId);
    const passwordField = document.querySelector(passwordFieldId);

    if (toggleButton && passwordField) {
        toggleButton.addEventListener("click", function () {
            // Toggle the type attribute (password to text and vice versa)
            const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
            passwordField.setAttribute("type", type);

            // Toggle the eye / eye-slash icon
            this.classList.toggle("fa-eye");
            this.classList.toggle("fa-eye-slash");
        });
    }
}

// Toggle for the login password field
togglePasswordVisibility("#toggle-password", "#password-field");

// Toggle for the register password field
togglePasswordVisibility("#toggle-register-password", "#register-password");

// Toggle for the confirm password field
togglePasswordVisibility("#toggle-confirm-password", "#confirm-password");
