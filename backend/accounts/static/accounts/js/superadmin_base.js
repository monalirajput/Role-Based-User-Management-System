document.addEventListener("DOMContentLoaded", function () {

    // ===== PROFILE DROPDOWN =====
    const profileIcon = document.querySelector(".profile-pill");
    const dropdown = document.getElementById("profileDropdown");

    if (profileIcon && dropdown) {
        profileIcon.addEventListener("click", function (e) {
            e.stopPropagation();
            dropdown.style.display =
                dropdown.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", function () {
            dropdown.style.display = "none";
        });
    }

    // ===== DARK MODE TOGGLE =====
    const darkBtn = document.getElementById("darkToggle");

    if (darkBtn) {
        darkBtn.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");
        });
    }

    // ===== AUTO HIDE SUCCESS POPUP =====
    setTimeout(function () {
        const popups = document.querySelectorAll(".success-popup");
        popups.forEach(function (popup) {
            popup.style.display = "none";
        });
    }, 3000);

});