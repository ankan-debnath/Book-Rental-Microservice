window.onload = async function () {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Please login to view your rentals.");
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
        const div = document.createElement("div");
        div.className = "rental-item";
        div.innerHTML = `
          <span>Rental ID: ${rental.id} | Book ID: ${rental.book_id}</span>
          <button class="return-btn" data-rental-id="${rental.id}" data-book-id="${rental.book_id}">Return Book</button>
        `;
        rentalList.appendChild(div);
      });

      // Add event listener for return book buttons
      const returnButtons = document.querySelectorAll(".return-btn");
      returnButtons.forEach(button => {
        button.addEventListener("click", async (e) => {
          const rentalId = e.target.getAttribute("data-rental-id");
          const bookId = e.target.getAttribute("data-book-id");
          await returnBook(rentalId, bookId);
        });
      });
    } else {
      rentalList.textContent = data.message || "Failed to load rental data.";
    }
  } catch (err) {
    console.error(err);
    document.getElementById("rentalList").textContent = "Error loading rental data.";
  }
};

// Return Book function
async function returnBook(rentalId, bookId) {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("You must be logged in to return a book.");
    window.location.href = "login.html";
    return;
  }
  if (isTokenExpired(token)) {
        localStorage.removeItem("access_token");
        message.textContent = "Token expired. Please try logging in again.";
        return;
      }

  try {
    const res = await fetch(`http://127.0.0.1:5000/v1/user/me/return/1/${bookId}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json"
      }
    });

    const data = await res.json();
    if (res.ok) {
      alert("Book returned successfully!");
      // Optionally, you could remove the rental from the list or reload the rentals
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
    localStorage.removeItem("access_token"); // Remove malformed token
    return true;
  }
}


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