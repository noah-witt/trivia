import { createApp } from 'vue'
import PrimeVue from 'primevue/config'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import 'primevue/resources/themes/aura-light-blue/theme.css'

createApp(App).use(router).use(PrimeVue).mount('#app')
