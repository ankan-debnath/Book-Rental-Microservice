document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  try {
    // Create a URLSearchParams object for form-encoded data
    const formData = new URLSearchParams();
    formData.append("username", username);  // Username field (email in this case)
    formData.append("password", password);  // Password field

    // Make a POST request to /token with form-encoded data
    const response = await fetch("http://127.0.0.1:5000/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",  // We are sending form-encoded data
      },
      body: formData  // Send formData in the request body
    });

    // Handle the response
    const data = await response.json();
    const message = document.getElementById("loginMessage");

    if (response.ok && data.access_token) {
      // If login is successful, store the token
      localStorage.setItem("access_token", data.access_token);
      message.textContent = "Login successful! Redirecting...";

      // Redirect to another page after a short delay
      setTimeout(() => {
        window.location.href = "profile.html";  // Redirect to books page
      }, 1000);
    } else {
      message.textContent = "Login failed. Please try again.";
    }

  } catch (error) {
    console.error("Error during login:", error);
  }
});
