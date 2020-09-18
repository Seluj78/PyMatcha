import Vue from 'vue';
import { ValidationProvider, ValidationObserver, extend } from 'vee-validate/dist/vee-validate.full.esm';
import App from './App.vue';
import router from './router';
import store from './store';
import validPassword from './validators/validPassword';
import './assets/css/tailwind.css';

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);
extend('validPassword', validPassword);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
