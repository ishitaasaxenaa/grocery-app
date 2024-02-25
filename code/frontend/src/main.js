import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { pinia } from './store/store.js'; // Import your Pinia store

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const app = createApp(App);

app.use(router);
app.use(pinia); // Use the Pinia store

app.mount('#app');
