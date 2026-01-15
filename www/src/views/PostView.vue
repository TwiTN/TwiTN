<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { apiFetch, readError } from '../api/client';
import { useAuth } from '../state/auth';
import PostCard from '../components/PostCard.vue';
import PostModal from '../components/PostModal.vue';

const route = useRoute();
const post = ref(null);
const parentChain = ref([]);
const loading = ref(true);
const error = ref('');
const replyModalOpen = ref(false);

const { currentUser } = useAuth();

const buildThread = (replies, depth = 0, acc = [], parent = null) => {
  replies.forEach((reply) => {
    acc.push({reply, depth, parent, parentHandle: parent?.author?.username || null});
    if (reply.replies && reply.replies.length > 0) {
      buildThread(reply.replies, depth + 1, acc, reply);
    }
  });
  return acc;
};

const threadReplies = computed(() => buildThread(post.value?.replies || [], 0, [], post.value));

const parentThread = computed(() => {
  if (!post.value) {
    return [];
  }
  const chain = parentChain.value || [];
  const items = chain.map((parent, index) => ({
    post: parent,
    depth: index,
    parentHandle: index > 0 ? chain[index - 1]?.author?.username || null : null,
    isCurrent: false,
  }));
  const parentHandle = chain.length ? chain[chain.length - 1]?.author?.username || null : null;
  items.push({
    post: post.value,
    depth: chain.length,
    parentHandle,
    isCurrent: true,
  });
  return items;
});

const fetchPostById = async (postId) => {
  const res = await apiFetch(`/api/posts/${postId}?depth=0`);
  if (!res.ok) {
    return null;
  }
  return res.json();
};

const loadParentChain = async (currentPost) => {
  parentChain.value = [];
  if (!currentPost || !currentPost.response_to) {
    return;
  }

  const chain = [];
  const seen = new Set([currentPost.id]);
  let nextId = currentPost.response_to;

  while (nextId && !seen.has(nextId)) {
    seen.add(nextId);
    const parent = await fetchPostById(nextId);
    if (!parent) {
      break;
    }
    chain.push(parent);
    nextId = parent.response_to;
  }

  parentChain.value = chain.reverse();
};

const loadPost = async () => {
  loading.value = true;
  error.value = '';
  post.value = null;
  parentChain.value = [];
  try {
    const res = await apiFetch(`/api/posts/${route.params.id}?depth=1`);
    if (res.ok) {
      post.value = await res.json();
      await loadParentChain(post.value);
    } else {
      error.value = (await readError(res)) || 'Post introuvable.';
    }
  } catch (err) {
    error.value = 'Erreur réseau.';
  } finally {
    loading.value = false;
  }
};

const openReply = () => {
  replyModalOpen.value = true;
};

const closeReply = () => {
  replyModalOpen.value = false;
};

onMounted(loadPost);
watch(
  () => route.params.id,
  () => {
    loadPost();
  }
);
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-6 px-4 py-8">
    <RouterLink to="/" class="text-white/70 hover:text-white">
      <span class="material-icons-outlined text-[18px]">chevron_left</span>
      Retour au feed
    </RouterLink>

    <div v-if="loading" class="text-white/70">Chargement...</div>
    <div v-else-if="error" class="text-amber-300">{{ error }}</div>
    <div v-else-if="post" class="space-y-6">
      <div v-if="parentChain.length" class="space-y-4">
        <div class="text-sm text-white/60">Fil parent</div>
        <div class="space-y-4">
          <div v-for="item in parentThread" :key="item.post.id" class="space-y-2">
            <div v-if="item.parentHandle" class="flex items-center gap-2 text-xs text-white/60">
              <span class="material-icons-outlined text-[16px]">subdirectory_arrow_right</span>
              <span>Réponse à</span>
              <RouterLink :to="`/user/${item.parentHandle}`" class="text-white/70 hover:text-white">
                @{{ item.parentHandle }}
              </RouterLink>
            </div>
            <div v-else class="flex items-center gap-2 text-xs text-white/50">
              <span class="material-icons-outlined text-[16px]">arrow_upward</span>
              <span>Tweet d'origine</span>
            </div>
            <div class="pl-4 border-l border-white/10" :style="{ marginLeft: `${item.depth * 16}px` }">
              <PostCard :post="item.post" :show-replies="false" :reload="loadPost" />
            </div>
          </div>
        </div>
        <div class="border-t border-white/10"></div>
      </div>

      <PostCard v-else :post="post" :show-replies="false" :reload="loadPost" />

      <div class="flex items-center gap-3">
        <button v-if="currentUser" type="button" class="btn btn-sm btn-outline border-white/30 text-white/80 hover:bg-white hover:text-black" @click="openReply">
          Répondre
        </button>
        <RouterLink v-else to="/login" class="btn btn-sm bg-white text-black hover:bg-white/80">
          Connexion
        </RouterLink>
        <span v-if="!currentUser" class="text-white/60 text-sm">Connecte-toi pour répondre.</span>
      </div>

      <div class="space-y-4">
        <h2 class="text-lg font-semibold text-white">Fil de réponses</h2>
        <div v-if="threadReplies.length === 0" class="text-white/70">
          Pas encore de réponses.
        </div>
        <div v-else class="space-y-4">
          <div v-for="item in threadReplies" :key="item.reply.id" class="space-y-2">
            <div class="flex items-center gap-2 text-xs text-white/60">
              <span class="material-icons-outlined text-[16px]">subdirectory_arrow_right</span>
              <span>Réponse à</span>
              <RouterLink v-if="item.parentHandle" :to="`/user/${item.parentHandle}`" class="text-white/70 hover:text-white">
                @{{ item.parentHandle }}
              </RouterLink>
              <span v-else class="text-white/50">tweet</span>
            </div>
            <div class="pl-4 border-l border-white/10" :style="{ marginLeft: `${item.depth * 16}px` }">
              <PostCard :post="item.reply" :show-replies="false" :reload="loadPost" />
            </div>
          </div>
        </div>
      </div>

      <PostModal :open="replyModalOpen" :reply-to="post.id" title="Répondre" @close="closeReply" @posted="loadPost"/>
    </div>
  </div>
</template>
