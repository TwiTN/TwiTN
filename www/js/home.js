async function loadPosts() {
  const container = document.getElementById("posts");
  container.innerHTML = "<p class='text-center'>Chargement...</p>";

  try {
    const posts = await getPosts();
    container.innerHTML = "";

    if (posts.length === 0) {
      container.innerHTML =
        "<p class='text-center opacity-70'>Aucun post pour le moment</p>";
      return;
    }

    posts.forEach((post) => {
      const card = document.createElement("div");
      card.className = "card bg-base-100 shadow-md";

      card.innerHTML = `
        <div class="card-body">
          <h2 class="card-title">${post.title}</h2>
          <p>${post.content}</p>
          <div class="card-actions justify-end">
            <a href="post.html?id=${post.id}" class="btn btn-sm btn-primary">
              Voir
            </a>
          </div>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML =
      "<p class='text-center text-error'>Erreur de chargement des posts</p>";
    console.error(err);
  }
}

loadPosts();
