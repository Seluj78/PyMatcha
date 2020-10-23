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

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
