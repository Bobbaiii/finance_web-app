import { ref, onMounted } from 'vue'

const THEME_STORAGE_KEY = 'theme'
const isDarkMode = ref(false)
let isInitialized = false

const applyTheme = (dark) => {
  if (typeof document === 'undefined') return
  const root = document.documentElement

  if (dark) {
    root.classList.add('dark')
    localStorage.setItem(THEME_STORAGE_KEY, 'dark')
  } else {
    root.classList.remove('dark')
    localStorage.setItem(THEME_STORAGE_KEY, 'light')
  }
}

const detectInitialTheme = () => {
  if (typeof window === 'undefined') return false

  const stored = localStorage.getItem(THEME_STORAGE_KEY)
  if (stored) {
    return stored === 'dark'
  }

  if (window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  return false
}

const initializeTheme = () => {
  if (isInitialized) return
  const dark = detectInitialTheme()
  isDarkMode.value = dark
  applyTheme(dark)
  isInitialized = true
}

export const useTheme = () => {
  onMounted(() => {
    initializeTheme()
  })

  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value
    applyTheme(isDarkMode.value)
  }

  const setTheme = (dark) => {
    isDarkMode.value = dark
    applyTheme(dark)
  }

  return {
    isDarkMode,
    toggleTheme,
    setTheme,
    initializeTheme
  }
}
