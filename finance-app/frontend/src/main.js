import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import './assets/css/tailwind.css' // Si vous utilisez Tailwind CSS

const app = createApp(App)

app.use(router)
app.use(store)
app.use(Toast)

app.mount('#app')
