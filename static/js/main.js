// Example: Form validation
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('#login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.querySelector('#username').value;
            const password = document.querySelector('#password').value;
            if (!username || !password) {
                e.preventDefault();
                alert('Please fill in all fields');
            }
        });
    }
});

// Add more JavaScript functions as needed
