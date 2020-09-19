import Vue from 'vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate/dist/vee-validate.full.esm';
import http from './plugins/http';
import errorMessenger from './plugins/errorMessenger';
import App from './App.vue';
import router from './router';
import store from './store';
import validPassword from './validators/validPassword';
import './assets/css/tailwind.css';

import * as Sentry from "@sentry/browser";
import { Vue as VueIntegration } from "@sentry/integrations";
import { Integrations } from "@sentry/tracing";

Sentry.init({
  dsn: "https://fc31e918801742e2b1e691067496e257@o450203.ingest.sentry.io/5434440",
  integrations: [
    new VueIntegration({
      Vue,
      tracing: true,
    }),
    new Integrations.BrowserTracing(),
  ],
  tracesSampleRate: 1,
});

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);
extend('validPassword', validPassword);

Vue.config.productionTip = false;

Vue.use(http);
Vue.use(errorMessenger);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
