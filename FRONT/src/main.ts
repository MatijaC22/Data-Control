//npm run dev
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import VeeValidatePlugin from './includes/validation';

loadFonts()

createApp(App)
  .use(router)
  .use(createPinia())
  .use(vuetify)
  .use(VeeValidatePlugin)
  .mount('#app')
