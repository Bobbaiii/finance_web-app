import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/css/tailwind.css' // Si vous utilisez Tailwind CSS

createApp(App).use(router).use(store).mount('#app')
