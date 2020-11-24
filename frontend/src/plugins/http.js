/* eslint-disable prefer-arrow-callback */
/* eslint-disable func-names */
/* eslint-disable no-param-reassign */

import Axios from 'axios';
import Vue from 'vue';
import { getAccessToken, getRefreshToken, handleAccessTokenExpiration } from '../auth/tokens';

Axios.defaults.baseURL = process.env.VUE_APP_BACKEND_BASE_URL;
Axios.defaults.headers.common['Content-Type'] = 'application/json';
Axios.defaults.headers.common.Accept = 'application/json';

Axios.interceptors.request.use(async function (config) {
  if (config.url === '/auth/refresh' || config.url === '/auth/refresh_revoke') {
    config.headers.Authorization = `Bearer ${getRefreshToken()}`;
  } else if (config.url === '/auth/access_revoke') {
    config.headers.Authorization = `Bearer ${getAccessToken()}`;
  } else if (config.accessTokenRequired) {
    await handleAccessTokenExpiration();
    if (getAccessToken()) {
      config.headers.Authorization = `Bearer ${getAccessToken()}`;
    } else {
      window.location.reload();
      return { headers: {}, method: config.method, url: '' };
    }
  }
  if (config.url.search('/profile/images') !== -1) {
    config.headers['Content-Type'] = 'multipart/form-data';
  }
  delete config.accessTokenRequired;
  return config;
}, function (error) {
  return Promise.reject(error);
});

export default {
  install() {
    Vue.prototype.$http = Axios;
  },
};
