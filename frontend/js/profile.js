const API_URL = import.meta.env.API_URL;
console.log(API_URL)
  

document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Please login to view your profile.");
    window.location.href = "login.html";
    return;
  }

  // Check if the token is expired
  if (isTokenExpired(token)) {
    localStorage.removeItem("access_token");
    const message = document.getElementById("profileCard");
    message.textContent = "Token expired. Please try logging in again.";
    return;
  }

  // Fetch the user profile from the backend
  const response = await fetch("http://127.0.0.1:5000/v1/user/me", {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Accept": "application/json"
    }
  });

  const result = await response.json();
  const card = document.getElementById("profileCard");

  if (response.ok && result.success) {
    const user = result.data;
    card.innerHTML = `
      <p><strong>User ID:</strong> ${user.user_id}</p>
      <p><strong>Name:</strong> ${user.name}</p>
      <p><strong>Email:</strong> ${user.email}</p>
    `;
  } else {
    card.innerHTML = `<p style="color: red; text-align: center;">Failed to load profile: ${result.message}</p>`;
  }
});

// Function to check if the token is expired
function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp < currentTime;
  } catch (err) {
    localStorage.removeItem("access_token"); // Remove malformed token
    return true;
  }
}

// Logout function
function logout() {
  localStorage.removeItem("access_token"); // Remove the token
  window.location.href = "../index.html";  // Redirect to homepage or login page
}
