window.addEventListener('load', function () {
    setTimeout(function () {
        var body = document.body;
        var html = document.documentElement;
        var loader = document.getElementById('loader');
        var content = document.getElementById('root');

        loader.classList.add('fade-out');
        setTimeout(() => {
            loader.style.display = 'none';
            content.style.display = 'block';
        }, 500); // Wait for fade-out to complete
    }, 500);
});


// Function to show a page and save it to localStorage
function showPage(activePage) {
    // Get all pages dynamically
    const allPages = ["page1", "page2", "page3", "page4", "page5", "page6", "page7"];

    // Hide all pages
    allPages.forEach(page => document.getElementById(page)?.classList.remove("active"));

    // Show the selected page
    document.getElementById(activePage)?.classList.add("active");

    // Store the active page in localStorage
    localStorage.setItem("activePage", activePage);
}

// On page load, check if there’s a saved page and show it
document.addEventListener("DOMContentLoaded", function () {
    const savedPage = localStorage.getItem("activePage") || "page1"; // Default to page1
    showPage(savedPage);
});


// Ensure the script runs after the DOM has loaded
document.addEventListener('DOMContentLoaded', function () {
    const showPasswordCheckbox = document.getElementById('show-password');
    const passwordInput = document.getElementById('password');

    // Add an event listener to toggle password visibility
    showPasswordCheckbox.addEventListener('change', function () {
        if (showPasswordCheckbox.checked) {
            passwordInput.type = 'text';  // Show password
        } else {
            passwordInput.type = 'password';  // Hide password
        }
    });
});


// Automatically hide the alert after 3 seconds
setTimeout(function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        alert.classList.add('hide');
    });
}, 3000);