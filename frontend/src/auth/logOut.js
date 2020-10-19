/* eslint-disable import/prefer-default-export */
import Axios from 'axios';

export const logOut = async () => {
  await Axios.post('/auth/logout', {
    access_token: localStorage.getItem(process.env.VUE_APP_ACCESS_TOKEN),
    refresh_token: localStorage.getItem(process.env.VUE_APP_REFRESH_TOKEN),
  });
  localStorage.removeItem(process.env.VUE_APP_ACCESS_TOKEN);
  localStorage.removeItem(process.env.VUE_APP_REFRESH_TOKEN);
  localStorage.removeItem(process.env.VUE_APP_VUEX_PERSISTED_STATE);
  localStorage.removeItem(process.env.VUE_APP_SECURE_LS_METADATA);
  await this.$store.dispatch('logout');
  await this.$router.push('/accounts/signin');
};
