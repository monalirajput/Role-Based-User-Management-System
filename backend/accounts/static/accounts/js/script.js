// Toggle Login Password
function toggleLoginPassword() {
    var passwordField = document.getElementById("loginPassword");

    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}

// Toggle Register Password
function toggleRegisterPassword() {
    var passwordField = document.getElementById("registerPassword");

    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}
