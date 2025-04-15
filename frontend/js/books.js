document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("You must be logged in to view the books.");
    window.location.href = "login.html";
    return;
  }

  // Fetch all books
  try {
    const response = await fetch("http://127.0.0.1:5000/v1/user/me/books/all", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    const result = await response.json();
    if (response.ok && result.data) {
      displayBooks(result.data);
    } else {
      alert("Failed to fetch books.");
    }
  } catch (err) {
    console.error("Error fetching books:", err);
    alert("An error occurred while fetching books.");
  }
});

function displayBooks(books) {
  const bookList = document.getElementById("bookList");

  books.forEach((book) => {
    const bookCard = document.createElement("div");
    bookCard.classList.add("book-card");

    bookCard.innerHTML = `
      <h3>${book.name}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Genre:</strong> ${book.genre}</p>
      <p><strong>Available Copies:</strong> ${book.available_copies}</p>
      <button class="rent-btn" data-book-id="${book.book_id}">Rent Book</button>
    `;

    // Append book card to the list
    bookList.appendChild(bookCard);

    // Rent button event
    bookCard.querySelector(".rent-btn").addEventListener("click", async () => {
      const copies = prompt("Enter the number of copies to rent:");
      if (copies) {
        await rentBook(book.book_id, copies);
      }
    });
  });
}

async function rentBook(bookId, copies) {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("You must be logged in to rent a book.");
    window.location.href = "login.html";
    return;
  }
  if (isTokenExpired(token)) {
        localStorage.removeItem("access_token");
        message.textContent = "Token expired. Please try logging in again.";
        return;
      }

  try {
    const res = await fetch(`http://127.0.0.1:5000/v1/user/me/rent/${copies}/${bookId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
    });

    const result = await res.json();
    if (res.ok) {
      alert("Book rented successfully!");
      window.location.reload();
    } else {
      alert(result.message || "Failed to rent the book.");
    }
  } catch (err) {
    console.error("Rent book error:", err);
    alert("An error occurred while renting the book.");
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