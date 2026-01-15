<script setup>
import { computed } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import ReactionBar from './ReactionBar.vue';

const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  showReplies: {
    type: Boolean,
    default: true,
  },
  reload: {
    type: Function,
    required: true,
  },
});

const authorName = computed(() => {
  if (!props.post.author) {
    return 'Utilisateur';
  }
  return props.post.author.display_name || props.post.author.username || 'Utilisateur';
});

const authorHandle = computed(() => {
  if (!props.post.author) {
    return 'unknown';
  }
  return props.post.author.username || 'unknown';
});

const postDate = computed(() => {
  const value = props.post?.posted_at ?? props.post?.postedAt;
  if (!value) {
    return null;
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date;
});

const formattedDate = computed(() => {
  const date = postDate.value;
  if (!date) {
    return '';
  }
  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
});

const relativeDate = computed(() => {
  const date = postDate.value;
  if (!date) {
    return '';
  }
  const diffMs = Date.now() - date.getTime();
  if (diffMs < 0 || diffMs >= 24 * 60 * 60 * 1000) {
    return '';
  }
  const rtf = new Intl.RelativeTimeFormat('fr-FR', { numeric: 'auto' });
  const diffSeconds = Math.floor(diffMs / 1000);
  if (diffSeconds < 60) {
    return rtf.format(-diffSeconds, 'second');
  }
  const diffMinutes = Math.floor(diffSeconds / 60);
  if (diffMinutes < 60) {
    return rtf.format(-diffMinutes, 'minute');
  }
  const diffHours = Math.floor(diffMinutes / 60);
  return rtf.format(-diffHours, 'hour');
});

const displayDate = computed(() => relativeDate.value || formattedDate.value);
const dateTooltip = computed(() => (relativeDate.value ? formattedDate.value : ''));

const totalReplies = computed(() => {
  const stack = Array.isArray(props.post.replies) ? [...props.post.replies] : [];
  let count = 0;

  while (stack.length > 0) {
    const current = stack.pop();
    if (!current) {
      continue;
    }
    count += 1;
    if (Array.isArray(current.replies) && current.replies.length > 0) {
      stack.push(...current.replies);
    }
  }

  return count;
});

const router = useRouter();

const openPost = () => {
  router.push(`/post/${props.post.id}`);
};

const openReply = () => {
  router.push({
    name: 'post',
    params: { id: props.post.id },
    query: { reply: '1' },
  });
};
</script>

<template>
  <article class="card bg-black/20 border border-white/10 shadow-xl cursor-pointer transition-colors duration-150 hover:bg-white/5" @click="openPost">
    <div class="card-body gap-4">
      <div class="flex items-start gap-4">
        <img src="/res/user-200.png" alt="User avatar" class="w-12 h-12 rounded-full" />
        <div class="flex-1 min-w-0 space-y-2 pr-16">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-sm font-semibold text-white">{{ authorName }}</div>
              <div v-if="post.response_to" class="text-xs text-white/60">
                Réponse à <span class="font-mono">@{{ post.response_to || 'unknown' }}</span>
              </div>
              <RouterLink :to="`/user/${authorHandle}`" class="text-xs text-white/60 hover:text-white/80" @click.stop>
                @{{ authorHandle }}
              </RouterLink>
            </div>
            <div v-if="displayDate" class="text-xs text-white/50" :class="relativeDate ? 'tooltip tooltip-top' : ''" :data-tip="relativeDate ? formattedDate : null">
              {{ displayDate }}
            </div>
          </div>

          <div>
            <h3 class="text-lg font-semibold text-white break-words [overflow-wrap:anywhere]">
              {{ post.title }}
            </h3>
            <p class="text-white/80 whitespace-pre-line break-words [overflow-wrap:anywhere]">
              {{ post.content }}
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-3" @click.stop>
            <button v-if="showReplies" type="button" class="flex items-center gap-2 text-xs text-white/60 transition-colors hover:text-white" aria-label="Repondre a ce post" @click.stop="openReply">
              <span class="material-symbols-outlined text-[18px]">chat_bubble</span>
              <span>{{ totalReplies }}</span>
            </button>
            <ReactionBar :post="post" :reload="props.reload" />
          </div>
        </div>
      </div>
    </div>
  </article>
</template>