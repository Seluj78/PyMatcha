import Vue from 'vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate/dist/vee-validate.full.esm';
import http from './plugins/http';
import errorMessenger from './plugins/errorMessenger';
import App from './App.vue';
import router from './router';
import store from './store';
import validPassword from './validators/validPassword';
import './assets/css/tailwind.css';

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);
extend('validPassword', validPassword);

Vue.config.productionTip = false;

Vue.use(http);
Vue.use(errorMessenger);

function envHasNecessaryVariables() {
  return !(!process.env.VUE_APP_BACKEND_BASE_URL
    || !process.env.VUE_APP_ACCESS_TOKEN
    || !process.env.VUE_APP_REFRESH_TOKEN
    || !process.env.VUE_APP_VUEX_PERSISTED_STATE
    || !process.env.VUE_APP_SECURE_LS_METADATA);
}

if (envHasNecessaryVariables()) {
  new Vue({
    router,
    store,
    render: (h) => h(App),
  }).$mount('#app');
} else {
  console.log('Environment variables missing. Please, set VUE_APP_BACKEND_BASE_URL,'
    + 'VUE_APP_ACCESS_TOKEN, VUE_APP_REFRESH_TOKEN, VUE_APP_VUEX_PERSISTED_STATE,'
    + 'VUE_APP_SECURE_LS_METADATA variables in .env file of frontend folder');
}
