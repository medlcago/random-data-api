import {createApp} from 'vue'
import App from './App.vue'
import PrimeVue from "primevue/config";
import 'primevue/resources/themes/aura-light-green/theme.css'
import './index.css'
import router from "@/router/router.js";

const app = createApp(App);


app.use(PrimeVue);
app.use(router);
app.mount('#app')
