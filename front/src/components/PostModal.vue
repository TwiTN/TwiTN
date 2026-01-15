<script setup>
import PostComposer from './PostComposer.vue';

const props = defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  replyTo: {
    type: String,
    default: null,
  },
  title: {
    type: String,
    default: 'Nouveau post',
  },
});

const emit = defineEmits(['close', 'posted']);

const close = () => emit('close');

const handlePosted = (post) => {
  emit('posted', post);
  emit('close');
};
</script>

<template>
  <div v-if="open" class="modal modal-open">
    <div class="modal-box bg-black/90 border border-white/10 text-white relative">
      <button type="button" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" aria-label="Close" @click="close">
        X
      </button>
      <div class="text-sm text-white/60 mb-3">{{ title }}</div>
      <PostComposer :reply-to="replyTo" @posted="handlePosted" />
    </div>
    <div class="modal-backdrop" @click="close"></div>
  </div>
</template>
