import { ref } from "vue";
import { apiFetch, readError } from "../api/client";

const currentUser = ref(null);
const authReady = ref(false);

async function loadCurrentUser() {
  authReady.value = false;
  try {
    const res = await apiFetch("/api/user/");
    if (res.ok) {
      currentUser.value = await res.json();
    } else {
      currentUser.value = null;
    }
  } catch (err) {
    currentUser.value = null;
  } finally {
    authReady.value = true;
  }
}

async function login(credentials) {
  const res = await apiFetch("/api/user/login", {
    method: "POST",
    body: credentials,
  });

  if (res.ok) {
    currentUser.value = await res.json();
    return { ok: true };
  }

  return {
    ok: false,
    status: res.status,
    error: await readError(res),
  };
}

async function logout() {
  const res = await apiFetch("/api/user/logout", { method: "POST" });
  currentUser.value = null;
  return res.ok;
}

async function signup(payload) {
  const res = await apiFetch("/api/user/", {
    method: "POST",
    body: payload,
  });

  if (res.ok) {
    return { ok: true, user: await res.json() };
  }

  return {
    ok: false,
    status: res.status,
    error: await readError(res),
  };
}

export function useAuth() {
  return { currentUser, authReady, loadCurrentUser, login, logout, signup };
}
