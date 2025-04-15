document.getElementById("updateForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("You must be logged in to update your profile.");
    window.location.href = "login.html";
    return;
  }

  if (isTokenExpired(token)) {
        localStorage.removeItem("access_token");
        message.textContent = "Token expired. Please try logging in again.";
        return;
      }

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const payload = { name, email };
  if (password) payload.password = password;

  try {
    const res = await fetch("http://127.0.0.1:5000/v1/user/me", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    });

    const result = await res.json();
    if (res.ok) {
      alert("Profile updated successfully.");
      window.location.href = "profile.html";
    } else {
      alert(result.message || "Failed to update profile.");
    }
  } catch (err) {
    console.error("Update error:", err);
    alert("An error occurred while updating profile.");
  }
});


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
