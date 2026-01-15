<script setup>
import { reactive, ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import { useAuth } from '../state/auth';

const router = useRouter();
const { signup } = useAuth();

const username = ref('');
const displayName = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const error = ref('');
const loading = ref(false);
const fieldErrors = reactive({
  username: '',
  displayName: '',
  email: '',
  password: '',
  confirmPassword: '',
});
const touched = reactive({
  username: false,
  displayName: false,
  email: false,
  password: false,
  confirmPassword: false,
});

const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

const validateField = (field) => {
  switch (field) {
    case 'username': {
      const value = username.value.trim();
      if (!value) return "Nom d'utilisateur requis.";
      if (value.length < 5 || value.length > 20) return 'Entre 5 et 20 caractères.';
      return '';
    }
    case 'displayName': {
      const value = displayName.value.trim();
      if (!value) return "Nom d'affichage requis.";
      if (value.length > 50) return 'Maximum 50 caractères.';
      return '';
    }
    case 'email': {
      const value = email.value.trim();
      if (!value) return 'Email requis.';
      if (value.length > 100) return 'Maximum 100 caractères.';
      if (!emailPattern.test(value)) return 'Email invalide.';
      return '';
    }
    case 'password': {
      const value = password.value;
      if (!value) return 'Mot de passe requis.';
      if (value.length < 8) return 'Minimum 8 caractères.';
      return '';
    }
    case 'confirmPassword': {
      const value = confirmPassword.value;
      if (!value) return 'Confirmation requise.';
      if (value.length < 8) return 'Minimum 8 caractères.';
      if (value !== password.value) return 'Les mots de passe ne correspondent pas.';
      return '';
    }
    default:
      return '';
  }
};

const validateAll = () => {
  let isValid = true;
  Object.keys(fieldErrors).forEach((field) => {
    const message = validateField(field);
    fieldErrors[field] = message;
    if (message) {
      isValid = false;
    }
  });
  return isValid;
};

const handleBlur = (field) => {
  touched[field] = true;
  fieldErrors[field] = validateField(field);
};

const handleInput = (field) => {
  if (touched[field]) {
    fieldErrors[field] = validateField(field);
  }
  if (field === 'password' && touched.confirmPassword) {
    fieldErrors.confirmPassword = validateField('confirmPassword');
  }
};

const submit = async () => {
  error.value = '';

  Object.keys(touched).forEach((field) => {
    touched[field] = true;
  });

  if (!validateAll()) {
    return;
  }

  loading.value = true;
  const result = await signup({
    username: username.value.trim(),
    display_name: displayName.value.trim(),
    email: email.value.trim(),
    password: password.value,
  });
  loading.value = false;

  if (result.ok) {
    router.push('/login');
    return;
  }

  if (result.status === 409) {
    error.value = "Nom d'utilisateur ou email déjà utilisé.";
    return;
  }

  error.value = result.error || 'Erreur lors de la création du compte.';
};
</script>

<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4 py-12">
    <div class="card w-full max-w-md backdrop-blur-lg bg-white/5 border border-white/10 shadow-lg">
      <div class="card-body space-y-5">
        <div class="space-y-2">
          <RouterLink to="/" class="flex items-center text-gray-400 hover:text-gray-300">
            <span class="material-icons-outlined">chevron_left</span>
            <span class="font-medium text-xs">Retour</span>
          </RouterLink>
          <h1 class="text-white text-2xl font-bold">S'inscrire</h1>
        </div>

        <div class="form-control">
          <div class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-visible">
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4">person</span>
            <input v-model="username" type="text" placeholder="Nom d'utilisateur" minlength="5" maxlength="20" aria-describedby="usernameError" :aria-invalid="fieldErrors.username ? 'true' : 'false'"
              :class="[
                'input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full',
                fieldErrors.username ? 'input-error' : '',
              ]"
              @keyup.enter="submit" @input="handleInput('username')" @blur="handleBlur('username')"/>
            <div class="tooltip tooltip-left" data-tip="5 à 20 caractères">
              <span class="material-icons-outlined text-white/60 text-[18px] pr-4">info</span>
            </div>
          </div>
          <span id="usernameError" class="mt-1 text-xs text-amber-300" v-show="fieldErrors.username">
            {{ fieldErrors.username }}
          </span>
        </div>

        <div class="form-control">
          <div class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-visible">
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4">badge</span>
            <input v-model="displayName" type="text" placeholder="Nom d'affichage" maxlength="50" aria-describedby="displayNameError" :aria-invalid="fieldErrors.displayName ? 'true' : 'false'"
              :class="[
                'input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full',
                fieldErrors.displayName ? 'input-error' : '',
              ]"
              @keyup.enter="submit" @input="handleInput('displayName')" @blur="handleBlur('displayName')"/>
            <div class="tooltip tooltip-left" data-tip="Max 50 caractères">
              <span class="material-icons-outlined text-white/60 text-[18px] pr-4">info</span>
            </div>
          </div>
          <span id="displayNameError" class="mt-1 text-xs text-amber-300" v-show="fieldErrors.displayName">
            {{ fieldErrors.displayName }}
          </span>
        </div>

        <div class="form-control">
          <div class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-visible">
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4">email</span>
            <input v-model="email"  type="email" placeholder="Email" maxlength="100" aria-describedby="emailError" :aria-invalid="fieldErrors.email ? 'true' : 'false'"
              :class="[
                'input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full',
                fieldErrors.email ? 'input-error' : '',
              ]"
              @keyup.enter="submit" @input="handleInput('email')" @blur="handleBlur('email')"/>
            <div class="tooltip tooltip-left" data-tip="Email valide">
              <span class="material-icons-outlined text-white/60 text-[18px] pr-4">info</span>
            </div>
          </div>
          <span id="emailError" class="mt-1 text-xs text-amber-300" v-show="fieldErrors.email">
            {{ fieldErrors.email }}
          </span>
        </div>

        <div class="form-control">
          <div class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-visible">
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4">password</span>
            <input v-model="password" type="password" placeholder="Mot de passe" minlength="8" aria-describedby="passwordError" :aria-invalid="fieldErrors.password ? 'true' : 'false'"
              :class="[
                'input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full',
                fieldErrors.password ? 'input-error' : '',
              ]"
              @keyup.enter="submit" @input="handleInput('password')" @blur="handleBlur('password')"/>
            <div class="tooltip tooltip-left" data-tip="Minimum 8 caractères">
              <span class="material-icons-outlined text-white/60 text-[18px] pr-4">info</span>
            </div>
          </div>
          <span id="passwordError" class="mt-1 text-xs text-amber-300" v-show="fieldErrors.password">
            {{ fieldErrors.password }}
          </span>
        </div>

        <div class="form-control">
          <div class="flex items-center bg-black/10 border border-white/10 rounded-lg overflow-visible">
            <span class="material-icons-outlined text-white/70 text-[20px] pl-4">password</span>
            <input
              v-model="confirmPassword" type="password" placeholder="Confirmer le mot de passe" minlength="8" aria-describedby="confirmPasswordError" :aria-invalid="fieldErrors.confirmPassword ? 'true' : 'false'"
              :class="[
                'input bg-transparent text-white placeholder-white/70 border-none focus:outline-none w-full',
                fieldErrors.confirmPassword ? 'input-error' : '',
              ]"
              @keyup.enter="submit" @input="handleInput('confirmPassword')" @blur="handleBlur('confirmPassword')"/>
            <div class="tooltip tooltip-left" data-tip="Doit correspondre">
              <span class="material-icons-outlined text-white/60 text-[18px] pr-4">info</span>
            </div>
          </div>
          <span id="confirmPasswordError" class="mt-1 text-xs text-amber-300" v-show="fieldErrors.confirmPassword">
            {{ fieldErrors.confirmPassword }}
          </span>
        </div>

        <div v-if="error" class="text-amber-300 text-sm">{{ error }}</div>

        <button class="btn bg-white text-gray-800 font-semibold hover:bg-gray-100 border-none shadow-md transition" :disabled="loading" @click="submit">
          {{ loading ? 'Inscription...' : 'Valider' }}
          <span class="material-icons-outlined text-[20px]">chevron_right</span>
        </button>
      </div>
    </div>
  </div>
</template>
