async function loadPosts() {
  const posts = await getPosts();
  const container = document.getElementById("posts");

  posts.forEach(post => {
    const card = document.createElement("div");
    card.className = "card bg-base-100 shadow-md";

    card.innerHTML = `
      <div class="card-body">
        <h2 class="card-title">${post.title}</h2>
        <p>${post.content}</p>
      </div>
    `;

    container.appendChild(card);
  });
}

loadPosts();
