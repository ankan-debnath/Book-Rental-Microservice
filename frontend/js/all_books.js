window.onload = async function () {
  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Please login first.");
    window.location.href = "login.html";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/v1/user/me/books/all", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json"
      }
    });

    const result = await res.json();
    const booksContainer = document.getElementById("booksContainer");

    if (res.ok && Array.isArray(result.data)) {
      result.data.forEach(book => {
        const div = document.createElement("div");
        div.className = "book-card";
        div.innerHTML = `
          <h3>${book.name}</h3>
          <p><strong>Author:</strong> ${book.author}</p>
          <p><strong>Genre:</strong> ${book.genre}</p>
          <p><strong>Available Copies:</strong> ${book.available_copies}</p>
        `;
        booksContainer.appendChild(div);
      });
    } else {
      booksContainer.innerHTML = `<p>${result.message || "No books found."}</p>`;
    }
  } catch (error) {
    console.error("Failed to load books:", error);
    document.getElementById("booksContainer").textContent = "Error fetching books.";
  }
};

