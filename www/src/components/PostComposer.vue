<script setup>
import { computed, ref } from "vue";
import { apiFetch, readError } from "../api/client";

const props = defineProps({
  replyTo: {
    type: String,
    default: null,
  },
});

const emit = defineEmits(["posted"]);

const title = ref("");
const body = ref("");
const error = ref("");
const loading = ref(false);

const titleCount = computed(() => title.value.length);
const bodyCount = computed(() => body.value.length);
const canSubmit = computed(
  () =>
    title.value.trim().length > 0 &&
    body.value.trim().length > 0 &&
    !loading.value,
);

const submit = async () => {
  error.value = "";
  if (!canSubmit.value) {
    return;
  }

  loading.value = true;
  try {
    const payload = {
      title: title.value.trim(),
      body: body.value.trim(),
      reply_to: props.replyTo || null,
    };

    const res = await apiFetch("/api/posts/", {
      method: "POST",
      body: payload,
    });

    if (res.ok) {
      title.value = "";
      body.value = "";
      emit("posted", await res.json());
      return;
    }

    if (res.status === 401) {
      error.value = "Connexion requise pour publier.";
      return;
    }

    error.value = (await readError(res)) || "Erreur lors de la publication.";
  } catch (err) {
    error.value = "Erreur réseau.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="card bg-black/20 border border-white/10 shadow-xl">
    <div class="card-body space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold text-white">Nouveau post</h2>
        <div class="text-xs text-white/60">
          {{ titleCount }}/50 · {{ bodyCount }}/500
        </div>
      </div>

      <input
        v-model="title"
        type="text"
        maxlength="50"
        placeholder="Titre court"
        class="input input-bordered w-full bg-white/5 text-white placeholder-white/50 border-white/10"
      />
      <textarea
        v-model="body"
        maxlength="500"
        placeholder="Partage ton idée..."
        class="textarea textarea-bordered w-full min-h-[140px] bg-white/5 text-white placeholder-white/50 border-white/10"
      ></textarea>

      <div v-if="error" class="text-sm text-amber-300">{{ error }}</div>

      <div class="card-actions justify-end">
        <button
          class="btn bg-white text-black hover:bg-white/80"
          :disabled="!canSubmit"
          @click="submit"
        >
          {{ loading ? "Publication..." : "Publier" }}
        </button>
      </div>
    </div>
  </div>
</template>
