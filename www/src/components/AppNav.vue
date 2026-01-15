<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuth } from '../state/auth';

const { currentUser, logout } = useAuth();
const isLoggedIn = computed(() => !!currentUser.value);

const handleLogout = async () => {
  await logout();
};
</script>

<template>
  <nav class="navbar px-6 py-3 bg-black/30 border-b border-white/10 backdrop-blur-md text-white">
    <div class="flex-1 gap-3 items-center">
      <RouterLink class="btn btn-ghost normal-case text-lg" to="/">
        <img src="/res/logoTwiTN.svg" alt="Logo" class="w-8 h-8" />
        <span class="ml-2">Twi'TN</span>
      </RouterLink>
    </div>
    <div v-if="isLoggedIn" class="flex-none gap-2 items-center">
      <RouterLink :to="`/user/${currentUser.username}`" class="btn btn-ghost normal-case text-left px-3 mr-2">
        <img src="/res/user-200.png" alt="User" class="w-8 h-8 rounded-full" />
        <div class="ml-2">
          <div class="text-xs text-white/60">@{{ currentUser.username }}</div>
          <div class="text-sm font-semibold">
            {{ currentUser.display_name || currentUser.username }}
          </div>
        </div>
      </RouterLink>
      <button class="btn btn-outline border-white/40 text-white hover:bg-white hover:text-black" @click="handleLogout">
        Déconnexion
      </button>
    </div>
    <div v-else class="flex-none gap-2">
      <RouterLink to="/login" class="btn btn-outline border-white/40 text-white hover:bg-white hover:text-black mr-2">
        Connexion
      </RouterLink>
      <RouterLink to="/signup" class="btn bg-white text-black hover:bg-white/80">
        Inscription
      </RouterLink>
    </div>
  </nav>
</template>
