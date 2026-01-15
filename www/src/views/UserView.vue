<script setup>
import { onMounted, ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { apiFetch, readError } from '../api/client';
import PostCard from '../components/PostCard.vue';

const route = useRoute();
const user = ref(null);
const loading = ref(true);
const error = ref('');
const posts = ref([]);
const postsLoading = ref(false);
const postsError = ref('');

const loadPosts = async (username) => {
  postsLoading.value = true;
  postsError.value = '';
  posts.value = [];
  try {
    const res = await apiFetch('/api/posts/');
    if (res.ok) {
      const allPosts = await res.json();
      posts.value = allPosts.filter((post) => post.author?.username === username);
      return;
    }
    postsError.value = (await readError(res)) || 'Erreur lors du chargement des tweets.';
  } catch (err) {
    postsError.value = 'Erreur réseau.';
  } finally {
    postsLoading.value = false;
  }
};

const loadUser = async () => {
  loading.value = true;
  error.value = '';
  user.value = null;
  try {
    const res = await apiFetch(`/api/user/${route.params.username}`);
    if (res.ok) {
      user.value = await res.json();
      await loadPosts(user.value.username);
    } else {
      error.value = (await readError(res)) || 'Utilisateur introuvable.';
    }
  } catch (err) {
    error.value = 'Erreur réseau.';
  } finally {
    loading.value = false;
  }
};

onMounted(loadUser);
watch(
  () => route.params.username,
  () => {
    loadUser();
  }
);
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-6 px-4 py-8">
    <RouterLink to="/" class="text-white/70 hover:text-white">
      <span class="material-icons-outlined text-[18px]">chevron_left</span>
      Retour au feed
    </RouterLink>

    <div v-if="loading" class="text-white/70">Chargement...</div>
    <div v-else-if="error" class="text-amber-300">{{ error }}</div>
    <div v-else-if="user" class="space-y-6">
      <div class="card bg-black/20 border border-white/10 shadow-xl">
        <div class="card-body space-y-2">
          <div class="flex items-center gap-4">
            <img src="/res/user-200.png" alt="User avatar" class="w-16 h-16 rounded-full" />
            <div>
              <h1 class="text-2xl font-semibold text-white">
                {{ user.display_name || user.username }}
              </h1>
              <p class="text-white/60">@{{ user.username }}</p>
            </div>
          </div>
          <p class="text-white/80">Email: {{ user.email }}</p>
        </div>
      </div>

      <div class="space-y-4">
        <h2 class="text-lg font-semibold text-white">Tweets</h2>
        <div v-if="postsLoading" class="text-white/70">Chargement des tweets...</div>
        <div v-else-if="postsError" class="text-amber-300">{{ postsError }}</div>
        <div v-else-if="posts.length === 0" class="text-white/70">
          Aucun tweet pour le moment.
        </div>
        <div v-else class="space-y-4">
          <PostCard v-for="post in posts" :key="post.id" :post="post" />
        </div>
      </div>
    </div>
  </div>
</template>
