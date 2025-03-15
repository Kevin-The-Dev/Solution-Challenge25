document.addEventListener("DOMContentLoaded", function () {
    // Sample credentials (in a real app, this would be handled server-side)
    const validUsername = "user";
    const validPassword = "password";
   
  
    // Get DOM elements
    const loginForm = document.getElementById("login-form");
    const usernameInput = document.querySelector("input[type='text']");
    const passwordInput = document.querySelector("input[type='password']");
    const loginBtn = document.querySelector(".login-btn");
    const rememberCheckbox = document.getElementById("remember");
    const roleSelect = document.getElementById('role'); // Get the role select element
   
  
    // Check if there are saved credentials
    checkSavedCredentials();
   
  
    // Add input animations
    const inputGroups = document.querySelectorAll(".input-group");
    inputGroups.forEach(group => {
    const input = group.querySelector("input");
   
  
    // Initial check for pre-filled inputs
    if (input.value !== "") {
    group.classList.add("active");
    }
   
  
    input.addEventListener("focus", () => {
    group.classList.add("active");
    });
   
  
    input.addEventListener("blur", () => {
    if (input.value === "") {
    group.classList.remove("active");
    }
    });
    });
   
  
    // Create notification element
    const notification = document.createElement("div");
    notification.className = "notification";
    document.body.appendChild(notification);
   
  
    // Function to show notifications
    function showNotification(message, type) {
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = "block";
   
  
    // Add animation
    setTimeout(() => {
    notification.classList.add("show");
    }, 10);
   
  
    // Hide after 3 seconds
    setTimeout(() => {
    notification.classList.remove("show");
    setTimeout(() => {
    notification.style.display = "none";
    }, 300);
    }, 3000);
    }
   
  
    // Form submission handler
    loginForm.addEventListener("submit", function (e) {
    e.preventDefault();
   
  
    let username = usernameInput.value.trim();
    let password = passwordInput.value.trim();
    const role = document.getElementById('role').value; // Get the selected role
   
  
    // Add button animation
    loginBtn.classList.add("clicked");
    setTimeout(() => {
    loginBtn.classList.remove("clicked");
    }, 200);
   
  
    // Validate inputs
    if (username === "" || password === "") {
    showNotification("Please fill in both username and password fields.", "error");
    highlightEmptyFields(username, password);
    return;
    }
   
  
    // Simulate loading state
    loginBtn.disabled = true;
    loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
   
  
    // Simulate server request with timeout
    setTimeout(() => {
    if (username === validUsername && password === validPassword) {
    // Successful login
    showNotification("Login successful! Redirecting to dashboard...", "success");
   
  
    // Save credentials if remember me is checked
    if (rememberCheckbox.checked) {
    localStorage.setItem("savedUsername", username);
    } else {
    localStorage.removeItem("savedUsername");
    }
   
  
    // Add success animation to form
    loginForm.classList.add("success");
   
  
    // Simulate redirect after 2 seconds
    setTimeout(() => {
    // In a real app, you would redirect to another page based on the selected role
    if (role === 'teacher') {
    window.location.href = "teacher_db.html";
    } else if (role === 'student') {
    window.location.href = "students.html";
    }
   
  
    // For demo purposes, reset the form and button
    loginForm.classList.remove("success");
    resetForm();
    }, 2000);
    } else {
    // Failed login
    showNotification("Invalid username or password. Please try again.", "error");
   
  
    // Add error shake animation to form
    loginForm.classList.add("error");
    setTimeout(() => {
    loginForm.classList.remove("error");
    }, 500);
   
  
    // Reset button state
    loginBtn.disabled = false;
    loginBtn.innerHTML = '<span>Login Now</span><i class="fas fa-arrow-right"></i>';
   
  
    // Focus on username field
    usernameInput.focus();
    }
    }, 1500);
    });
   
  
    // Highlight empty fields with red border
    function highlightEmptyFields(username, password) {
    if (username === "") {
    inputGroups[0].classList.add("error-field");
    setTimeout(() => {
    inputGroups[0].classList.remove("error-field");
    }, 2000);
    }
   
  
    if (password === "") {
    inputGroups[1].classList.add("error-field");
    setTimeout(() => {
    inputGroups[1].classList.remove("error-field");
    }, 2000);
    }
    }
   
  
    // Reset form to initial state
    function resetForm() {
    usernameInput.value = "";
    passwordInput.value = "";
    loginBtn.disabled = false;
    loginBtn.innerHTML = '<span>Login Now</span><i class="fas fa-arrow-right"></i>';
    inputGroups.forEach(group => group.classList.remove("active"));
    }
   
  
    // Check for saved credentials
    function checkSavedCredentials() {
    const savedUsername = localStorage.getItem("savedUsername");
    if (savedUsername) {
    usernameInput.value = savedUsername;
    rememberCheckbox.checked = true;
    inputGroups[0].classList.add("active");
    // Focus on password field for better UX
    setTimeout(() => {
    passwordInput.focus();
    }, 500);
    }
    }
   
  
    // Social login buttons
    document.querySelector(".google").addEventListener("click", function () {
    showNotification("Google login initiated. Redirecting to Google...", "info");
    simulateSocialLogin("Google");
    });
   
  
    document.querySelector(".facebook").addEventListener("click", function () {
    showNotification("Facebook login initiated. Redirecting to Facebook...", "info");
    simulateSocialLogin("Facebook");
    });
   
  
    // Simulate social login
    function simulateSocialLogin(provider) {
    // Disable all buttons during "redirect"
    const buttons = document.querySelectorAll("button");
    buttons.forEach(btn => btn.disabled = true);
   
  
    // Show loading state
    setTimeout(() => {
    showNotification(`Successfully authenticated with ${provider}!`, "success");
   
  
    // Re-enable buttons
    setTimeout(() => {
    buttons.forEach(btn => btn.disabled = false);
    }, 2000);
    }, 2000);
    }
   
  
    // Forgot password link
    document.querySelector(".forgot-password").addEventListener("click", function (e) {
    e.preventDefault();
    showNotification("Password reset link has been sent to your email.", "info");
    });
   
  
    // Sign up link
    document.querySelector(".signup-link a").addEventListener("click", function (e) {
    e.preventDefault();
    showNotification("Sign up functionality coming soon!", "info");
    });
   });
  