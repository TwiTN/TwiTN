<script setup>
import { computed, onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';
import { apiFetch, readError } from '../api/client';
import { useAuth } from '../state/auth';
import PostCard from '../components/PostCard.vue';
import PostModal from '../components/PostModal.vue';

const posts = ref([]);
const loading = ref(true);
const error = ref('');

const { currentUser } = useAuth();
const feedPosts = computed(() => posts.value.filter((post) => post.response_to == null));
const postModalOpen = ref(false);

const loadPosts = async () => {
  loading.value = true;
  error.value = '';
  try {
    const res = await apiFetch('/api/posts/');
    if (res.ok) {
      posts.value = await res.json();
    } else {
      error.value = (await readError(res)) || 'Erreur lors du chargement du feed.';
    }
  } catch (err) {
    error.value = 'Erreur réseau.';
  } finally {
    loading.value = false;
  }
};

onMounted(loadPosts);

const openNewPost = () => {
  postModalOpen.value = true;
};

const closeNewPost = () => {
  postModalOpen.value = false;
};

const handlePosted = () => {
  loadPosts();
};
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6 px-4 py-8">
    <div class="card bg-black/40 border border-white/10 shadow-xl">
      <div class="card-body">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 class="text-3xl font-semibold text-white">Twi'TN</h1>
            <p class="text-white/70">
              Un micro réseau social pour poster, répondre et réagir en un clic.
            </p>
          </div>
          <button v-if="currentUser" type="button" class="btn btn-sm bg-white/10 border border-white/20 text-white hover:bg-white/20" @click="openNewPost">
            Quoi de neuf ?
          </button>
        </div>
      </div>
    </div>

    <div v-if="!currentUser" class="card bg-black/20 border border-white/10 shadow-xl">
      <div class="card-body">
        <p class="text-white/80">Connecte-toi pour publier et réagir.</p>
        <div class="card-actions">
          <RouterLink to="/login" class="btn bg-white text-black hover:bg-white/80">
            Connexion
          </RouterLink>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-white/70">Chargement...</div>
    <div v-else-if="error" class="text-amber-300">{{ error }}</div>
    <div v-else-if="feedPosts.length === 0" class="text-white/70">
      Aucun post pour le moment.
    </div>
    <div v-else class="space-y-4">
      <PostCard v-for="post in feedPosts" :key="post.id" :post="post" />
    </div>

    <button v-if="currentUser" type="button" class="btn btn-circle bg-white text-black hover:bg-white/80 fixed bottom-6 left-6 shadow-xl z-20 w-16 h-16 text-3xl" aria-label="Nouveau post" @click="openNewPost">
      <span class="leading-none">+</span>
    </button>

    <PostModal :open="postModalOpen" title="Nouveau post" @close="closeNewPost" @posted="handlePosted"/>
  </div>
</template>
