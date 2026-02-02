<script setup>
import { ref } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAuth } from "../state/auth";

const router = useRouter();
const { login } = useAuth();

const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const submit = async () => {
  error.value = "";
  loading.value = true;
  const result = await login({
    username: username.value,
    password: password.value,
  });
  loading.value = false;

  if (result.ok) {
    router.push("/");
    return;
  }

  if (result.status === 401) {
    error.value = "Nom d'utilisateur ou mot de passe incorrect.";
    return;
  }

  error.value = result.error || "Erreur lors de la connexion.";
};
</script>

<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4 py-12">
    <div
      class="card w-full max-w-md backdrop-blur-lg auth-card border border-white/10 shadow-lg"
    >
      <div class="card-body space-y-5">
        <div class="space-y-2">
          <RouterLink
            to="/"
            class="flex items-center text-gray-400 hover:text-gray-300"
          >
            <span class="material-icons-outlined">chevron_left</span>
            <span class="font-medium text-xs">Retour</span>
          </RouterLink>
          <h1 class="text-white text-2xl font-bold">Se connecter</h1>
        </div>

        <div class="form-control">
          <div
            class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-hidden"
          >
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4"
              >person</span
            >
            <input
              v-model="username"
              type="text"
              placeholder="Nom d'utilisateur"
              class="input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full"
              @keyup.enter="submit"
            />
          </div>
        </div>

        <div class="form-control">
          <div
            class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-hidden"
          >
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4"
              >password</span
            >
            <input
              v-model="password"
              type="password"
              placeholder="Mot de passe"
              class="input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full"
              @keyup.enter="submit"
            />
          </div>
        </div>

        <RouterLink
          to="/signup"
          class="flex items-center text-gray-400 hover:text-gray-300"
        >
          <span class="font-medium text-xs underline"
            >Pas de compte ? Inscris-toi</span
          >
          <span class="material-icons-outlined" style="font-size: 1.2rem"
            >arrow_outward</span
          >
        </RouterLink>

        <div v-if="error" class="text-amber-300 text-sm">{{ error }}</div>

        <button
          class="btn bg-white text-gray-800 font-semibold hover:bg-gray-100 border-none shadow-md transition"
          :disabled="loading"
          @click="submit"
        >
          {{ loading ? "Connexion..." : "Valider" }}
          <span class="material-icons-outlined text-[20px]">chevron_right</span>
        </button>
      </div>
    </div>
  </div>
</template>
