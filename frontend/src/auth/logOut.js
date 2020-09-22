/* eslint-disable import/prefer-default-export */
import Axios from 'axios';

export const logOut = async () => {
  await Axios.delete('/auth/access_revoke');
  await Axios.delete('/auth/refresh_revoke');
  localStorage.removeItem(process.env.VUE_APP_ACCESS_TOKEN);
  localStorage.removeItem(process.env.VUE_APP_REFRESH_TOKEN);
  localStorage.removeItem(process.env.VUE_APP_VUEX_PERSISTED_STATE);
  localStorage.removeItem(process.env.VUE_APP_SECURE_LS_METADATA);
  await this.$store.dispatch('logout');
  await this.$router.push('/accounts/signin');
};
