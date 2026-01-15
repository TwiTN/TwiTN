<script setup>
import { onMounted } from "vue";
import { RouterView } from "vue-router";
import { useAuth } from "./state/auth";
import AppFooter from "./components/AppFooter.vue";
import AppNav from "./components/AppNav.vue";

const { loadCurrentUser } = useAuth();

onMounted(() => {
  loadCurrentUser();
});
</script>

<template>
  <div class="min-h-screen flex flex-col text-white">
    <AppNav />
    <main class="flex-1 relative z-10">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>
