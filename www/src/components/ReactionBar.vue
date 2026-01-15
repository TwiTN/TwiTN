<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { apiFetch, readError } from '../api/client';

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  reload: {
    type: Function,
    required: true,
  },
});

const error = ref('');
const loading = ref(false);
const customEmoji = ref('');
const customError = ref('');
const dropdownRef = ref(null);

// Keep reactions to a single code point to match the API max_length=1.
const baseReactions = [
  { codepoint: 0x2764, label: 'Coeur', emojiPresentation: true },
  { codepoint: 0x1f44d, label: 'Pouce' },
  { codepoint: 0x1f602, label: 'Rire' },
  { codepoint: 0x1f62e, label: 'Choc' },
  { codepoint: 0x1f622, label: 'Pleur' },
  { codepoint: 0x1f525, label: 'Flamme' },
];

const defaultReactions = baseReactions.map((reaction) => {
  const emoji = String.fromCodePoint(reaction.codepoint);
  const display = reaction.emojiPresentation ? String.fromCodePoint(reaction.codepoint, 0xfe0f): emoji;
  return { emoji, display, label: reaction.label };
});

const defaultEmojiSet = new Set(defaultReactions.map((reaction) => reaction.emoji));
const emojiRegex = /\p{Extended_Pictographic}/u;

const visibleReactions = computed(() => {
  const items = [];
  defaultReactions.forEach((reaction) => {
    const count = props.post.reactions?.[reaction.emoji];
    if (count) {
      items.push({ ...reaction, count });
    }
  });

  Object.entries(props.post.reactions || {}).forEach(([emoji, count]) => {
    if (!count || defaultEmojiSet.has(emoji)) {
      return;
    }
    items.push({ emoji, display: emoji, label: 'Réaction', count });
  });

  return items;
});

const react = async (reaction) => {
  error.value = '';
  loading.value = true;
  try {
    const normalized = reaction.trim();
    const encoded = encodeURIComponent(normalized);
    const res = await apiFetch(`/api/posts/${props.post.id}/reactions/${encoded}`, {
      method: 'POST',
    });
    if (res.status === 401) {
      error.value = 'Connexion requise pour réagir.';
      return;
    }
    if (!res.ok && res.status !== 201) {
      error.value = (await readError(res)) || 'Action impossible.';
      return;
    }

    // reload
    await props.reload();
  } catch (err) {
    error.value = 'Erreur réseau.';
  } finally {
    loading.value = false;
  }
};

const validateCustomEmoji = () => {
  const value = customEmoji.value.trim();
  if (!value) {
    return 'Ajoute un emoji.';
  }
  if (Array.from(value).length !== 1) {
    return 'Un seul emoji est autorisé.';
  }
  if (!emojiRegex.test(value)) {
    return 'Emoji invalide.';
  }
  return '';
};

const submitCustom = async () => {
  customError.value = '';
  const message = validateCustomEmoji();
  if (message) {
    customError.value = message;
    return;
  }
  await react(customEmoji.value.trim());
  customEmoji.value = '';
};

const handleCustomInput = () => {
  if (customError.value) {
    customError.value = '';
  }
};

const handleDocumentClick = (event) => {
  if (!dropdownRef.value) {
    return;
  }
  if (!dropdownRef.value.contains(event.target)) {
    dropdownRef.value.open = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleDocumentClick);
});

onUnmounted(() => {
  document.removeEventListener('click', handleDocumentClick);
});
</script>

<template>
  <div class="flex flex-wrap items-center gap-2 text-sm text-white/80">
    <div v-if="visibleReactions.length" class="flex flex-wrap items-center gap-2">
      <div v-for="reaction in visibleReactions" :key="reaction.emoji" class="tooltip tooltip-top" :data-tip="reaction.label">
        <button class="btn btn-ghost btn-sm text-white/80 hover:text-white" :disabled="loading" @click="react(reaction.emoji)">
          <span class="text-lg">{{ reaction.display }}</span>
          <span class="text-xs text-white/60">{{ reaction.count }}</span>
        </button>
      </div>
    </div>

    <details ref="dropdownRef" class="dropdown dropdown-top">
      <summary class="btn btn-ghost btn-sm text-white/70 hover:text-white list-none normal-case">
        <span class="material-symbols-outlined normal-case">add_reaction</span>
      </summary>
      <div class="dropdown-content z-20 w-64 rounded-xl border border-white/10 bg-black/80 p-3 shadow-xl backdrop-blur">
        <div class="text-xs text-white/60 mb-2">Réagir avec</div>
        <div class="grid grid-cols-6 gap-2 mb-3">
          <button v-for="reaction in defaultReactions" :key="reaction.emoji" class="btn btn-ghost btn-xs" :disabled="loading" @click="react(reaction.emoji)">
            <span class="text-lg">{{ reaction.display }}</span>
          </button>
        </div>
        <div class="text-xs text-white/60 mb-1">Emoji personnalisé</div>
        <div class="flex items-center gap-2">
          <input v-model="customEmoji" type="text" maxlength="2" placeholder="emoji" class="input input-xs bg-white/10 text-white placeholder-white/50 border-white/10 w-20" @input="handleCustomInput" @keyup.enter="submitCustom"/>
          <button class="btn btn-xs bg-white text-black hover:bg-white/80" :disabled="loading" @click="submitCustom">
            Ajouter
          </button>
        </div>
        <div v-if="customError" class="text-xs text-amber-300 mt-1">{{ customError }}</div>
      </div>
    </details>

    <span v-if="error" class="text-xs text-amber-300">{{ error }}</span>
  </div>
</template>
