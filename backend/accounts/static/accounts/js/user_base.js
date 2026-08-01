// Open Plans Modal
function openPlans() {
    let expiredPopup = document.getElementById("expiredPopup");
    if (expiredPopup) expiredPopup.style.display = "none";

    let plansModal = document.getElementById("plansModal");
    if (plansModal) {
        plansModal.style.display = "block";
    } else {
        console.error("plansModal not found");
    }
}

// Open Payment Modal
function openPayment() {
    let paymentModal = document.getElementById("paymentModal");

    if (paymentModal) {
        paymentModal.style.display = "block";
    } else {
        console.error("paymentModal not found");
    }
}

// BUY NOW FUNCTION (🔥 FIXED)
function buyNow(planId) {

    fetch("/subscriptions/create-order/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: "plan_id=" + planId
    })
    .then(res => {
        if (!res.ok) throw new Error("Create order failed");
        return res.json();
    })
    .then(data => {

        var options = {
            key: data.key,
            amount: data.amount,
            currency: "INR",
            order_id: data.order_id,

            handler: function (response) {

                console.log("PAYMENT SUCCESS:", response);

                // ✅ IMPORTANT: FIXED URL HERE
                fetch("/subscriptions/verify-payment/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": getCSRFToken()
                    },
                    body:
                        "payment_id=" + response.razorpay_payment_id +
                        "&order_id=" + response.razorpay_order_id +
                        "&plan_id=" + planId
                })
                .then(res => res.json())
                .then(data => {

                    console.log("VERIFY RESPONSE:", data);

                    if (data.status === "success") {
                        alert("✅ Payment Successful!");

                        // ✅ FORCE REFRESH DASHBOARD
                        window.location.href = "/accounts/user-dashboard/";

                    } else {
                        alert("❌ Payment verification failed");
                    }
                })
                .catch(err => {
                    console.error("VERIFY ERROR:", err);
                    alert("Server error during verification");
                });
            }
        };

        var rzp = new Razorpay(options);
        rzp.open();
    })
    .catch(err => {
        console.error("ERROR:", err);
        alert("Something went wrong");
    });
}

// CSRF TOKEN
function getCSRFToken() {
    let token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) {
        return token.value;
    } else {
        console.error("CSRF token not found!");
        return "";
    }
}

// ===== DARK MODE TOGGLE =====

const darkBtn = document.getElementById("darkToggle");
const iconContainer = document.querySelector("#darkToggle");

darkBtn.addEventListener("click", function () {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        iconContainer.innerHTML = '<i data-lucide="sun"></i>';
        localStorage.setItem("theme", "dark");
    } else {
        iconContainer.innerHTML = '<i data-lucide="moon"></i>';
        localStorage.setItem("theme", "light");
    }

    lucide.createIcons(); // 🔥 re-render icons
});

/* Load saved theme */
window.onload = function () {

    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
        iconContainer.innerHTML = '<i data-lucide="sun"></i>';
    } else {
        iconContainer.innerHTML = '<i data-lucide="moon"></i>';
    }

    lucide.createIcons();
};

// ===== PROFILE DROPDOWN =====
const profileBtn = document.getElementById("profileBtn");
const dropdown = document.getElementById("profileDropdown");

/* Toggle dropdown */
profileBtn.addEventListener("click", function (e) {
    e.stopPropagation(); // prevent bubbling
    dropdown.classList.toggle("show");
});

/* Close when clicking outside */
document.addEventListener("click", function (e) {
    if (!profileBtn.contains(e.target)) {
        dropdown.classList.remove("show");
    }
});
