/* eslint-disable prefer-arrow-callback */
/* eslint-disable func-names */
/* eslint-disable no-param-reassign */

import Axios from 'axios';
import Vue from 'vue';
import { getAccessToken, getRefreshToken, handleAccessTokenExpiration } from '../auth/tokens';

Axios.defaults.baseURL = process.env.VUE_APP_BACKEND_BASE_URL;

Axios.interceptors.request.use(async function (config) {
  if (config.url === '/auth/refresh' || config.url === '/auth/refresh_revoke') {
    config.headers.Authorization = `Bearer ${getRefreshToken()}`;
  } else if (config.url === '/auth/access_revoke') {
    config.headers.Authorization = `Bearer ${getAccessToken()}`;
  } else if (getAccessToken()) {
    await handleAccessTokenExpiration();
    if (getAccessToken()) {
      config.headers.Authorization = `Bearer ${getAccessToken()}`;
    } else {
      return { headers: {}, method: config.method, url: '' };
    }
  }
  return config;
}, function (error) {
  return Promise.reject(error);
});

export default {
  install() {
    Vue.prototype.$http = Axios;
  },
};
