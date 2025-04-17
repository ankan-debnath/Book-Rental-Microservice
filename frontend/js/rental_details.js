window.onload = async function () {
  const token = localStorage.getItem("access_token");
  if (!token || isTokenExpired(token)) {
    alert("Please login to view your rentals.");
    localStorage.removeItem("access_token");
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/v1/user/me/rentals", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json"
      }
    });

    const data = await res.json();
    const rentalList = document.getElementById("rentalList");

    if (res.ok && Array.isArray(data.data)) {
      data.data.forEach(rental => {
        const rentalId = Object.keys(rental)[0];
        const book = rental[rentalId];

        const div = document.createElement("div");
        div.className = "rental-item";
        div.innerHTML = `
          <div>
            <small><strong>Order ID:</strong> ${rentalId}</small>
            <br><br>
            <strong>${book.name}</strong><br>
            <small>Author: ${book.author}</small><br>
            <small>Genre: ${book.genre}</small><br>
          </div>
          <button class="return-btn" data-rental-id="${rentalId}" data-book-id="${book.book_id}">Return</button>
        `;

        rentalList.appendChild(div);
      });

      // Handle return buttons
      document.querySelectorAll(".return-btn").forEach(button => {
        button.addEventListener("click", async (e) => {
          const rentalId = e.target.getAttribute("data-rental-id");
          const bookId = e.target.getAttribute("data-book-id");
          await returnBook(rentalId, bookId);
        });
      });
    } else {
      rentalList.textContent = data.message || "No rentals found.";
    }
  } catch (err) {
    console.error(err);
    document.getElementById("rentalList").textContent = "Error loading rentals.";
  }
};

async function returnBook(rentalId, bookId) {
  const token = localStorage.getItem("access_token");
  if (!token || isTokenExpired(token)) {
    alert("Session expired. Please login again.");
    localStorage.removeItem("access_token");
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/v1/user/me/return/${bookId}/1`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json"
      }
    });

    const data = await res.json();
    if (res.ok) {
      alert("Book returned successfully!");
      window.location.reload();
    } else {
      alert(data.message || "Failed to return the book.");
    }
  } catch (err) {
    console.error(err);
    alert("An error occurred while returning the book.");
  }
}

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    return payload.exp < currentTime;
  } catch (err) {
    return true;
  }
}
