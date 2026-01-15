const API_BASE = "http://localhost:8000";

async function getPosts() {
  const res = await fetch(`${API_BASE}/posts`);
  return res.json();
}
