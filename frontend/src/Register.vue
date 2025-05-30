<template>
  <div class="min-h-screen flex items-center justify-center bg-neutral-100 dark:bg-neutral-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-neutral-900 dark:text-white">
          Créer un compte
        </h2>
        <p class="mt-2 text-center text-sm text-neutral-600 dark:text-neutral-400">
          Ou
          <router-link to="/login" class="font-medium text-primary hover:text-primary-dark">
            connectez-vous à votre compte existant
          </router-link>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="register">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="full-name" class="sr-only">Nom complet</label>
            <input
              id="full-name"
              name="full_name"
              type="text"
              required
              v-model="fullName"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-700 placeholder-neutral-500 dark:placeholder-neutral-400 text-neutral-900 dark:text-white rounded-t-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm dark:bg-neutral-800"
              placeholder="Nom complet"
            />
          </div>
          <div>
            <label for="email-address" class="sr-only">Adresse email</label>
            <input
              id="email-address"
              name="email"
              type="email"
              autocomplete="email"
              required
              v-model="email"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-700 placeholder-neutral-500 dark:placeholder-neutral-400 text-neutral-900 dark:text-white focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm dark:bg-neutral-800"
              placeholder="Adresse email"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Mot de passe</label>
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="new-password"
              required
              v-model="password"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-700 placeholder-neutral-500 dark:placeholder-neutral-400 text-neutral-900 dark:text-white focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm dark:bg-neutral-800"
              placeholder="Mot de passe"
            />
          </div>
          <div>
            <label for="confirm-password" class="sr-only">Confirmer le mot de passe</label>
            <input
              id="confirm-password"
              name="confirm_password"
              type="password"
              autocomplete="new-password"
              required
              v-model="confirmPassword"
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-700 placeholder-neutral-500 dark:placeholder-neutral-400 text-neutral-900 dark:text-white rounded-b-md focus:outline-none focus:ring-primary focus:border-primary focus:z-10 sm:text-sm dark:bg-neutral-800"
              placeholder="Confirmer le mot de passe"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg
                v-if="!loading"
                class="h-5 w-5 text-primary-dark group-hover:text-primary-light"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fill-rule="evenodd"
                  d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                  clip-rule="evenodd"
                />
              </svg>
              <svg
                v-else
                class="animate-spin h-5 w-5 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            </span>
            {{ loading ? 'Inscription en cours...' : 'S\'inscrire' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Register',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()

    const fullName = ref('')
    const email = ref('')
    const password = ref('')
    const confirmPassword = ref('')
    const loading = computed(() => store.getters.isLoading)

    const isFormValid = computed(() => {
      return (
        fullName.value.trim() !== '' &&
        email.value.trim() !== '' &&
        password.value.trim() !== '' &&
        password.value === confirmPassword.value &&
        password.value.length >= 8
      )
    })

    const register = async () => {
      if (!isFormValid.value) {
        toast.error('Veuillez remplir correctement tous les champs')
        return
      }

      try {
        store.dispatch('setLoading', true)
        await store.dispatch('auth/register', {
          full_name: fullName.value,
          email: email.value,
          password: password.value
        })
        toast.success('Inscription réussie ! Vous pouvez maintenant vous connecter.')
        router.push('/login')
      } catch (error) {
        toast.error('Échec de l\'inscription: ' + (error.message || 'Une erreur est survenue'))
      } finally {
        store.dispatch('setLoading', false)
      }
    }

    return {
      fullName,
      email,
      password,
      confirmPassword,
      loading,
      isFormValid,
      register
    }
  }
}
</script>
