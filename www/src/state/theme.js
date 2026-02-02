import { computed, ref } from "vue";

const STORAGE_KEY = "twitn-theme";
const theme = ref("dark");

const applyTheme = (value) => {
  theme.value = value;
  document.documentElement.setAttribute("data-theme", value);
};

const getSystemTheme = () =>
  window.matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark";

const initTheme = () => {
  if (typeof window === "undefined") {
    return;
  }
  const saved = window.localStorage.getItem(STORAGE_KEY);
  const initial = saved || getSystemTheme();
  applyTheme(initial);
};

const setTheme = (value) => {
  if (typeof window === "undefined") {
    return;
  }
  applyTheme(value);
  window.localStorage.setItem(STORAGE_KEY, value);
};

const toggleTheme = () => {
  setTheme(theme.value === "dark" ? "light" : "dark");
};

export const useTheme = () => ({
  theme,
  setTheme,
  toggleTheme,
  isDark: computed(() => theme.value === "dark"),
});

export { initTheme };

