/* eslint-disable import/prefer-default-export */
import Axios from 'axios';
import router from '../router';
import store from '../store';

export const logOut = async () => {
  await store.dispatch('logout');
  await router.push('/accounts/signin');
  await Axios.post('/auth/logout', {
    access_token: localStorage.getItem(process.env.VUE_APP_ACCESS_TOKEN),
    refresh_token: localStorage.getItem(process.env.VUE_APP_REFRESH_TOKEN),
  });
  localStorage.removeItem(process.env.VUE_APP_ACCESS_TOKEN);
  localStorage.removeItem(process.env.VUE_APP_REFRESH_TOKEN);
  localStorage.removeItem(process.env.VUE_APP_VUEX_PERSISTED_STATE);
  localStorage.removeItem(process.env.VUE_APP_SECURE_LS_METADATA);
};
