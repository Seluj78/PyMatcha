/* eslint-disable prefer-arrow-callback */
/* eslint-disable func-names */
/* eslint-disable no-param-reassign */
/* eslint-disable max-len */

import Axios from 'axios';
import Vue from 'vue';
import { getAccessToken, getRefreshToken, handleAccessTokenExpiration } from '../auth/tokens';

Axios.defaults.baseURL = process.env.VUE_APP_BACKEND_BASE_URL;
Axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
Axios.defaults.headers.common['Access-Control-Allow-Methods'] = 'DELETE, POST, GET, OPTIONS';
/* Axios.defaults.headers.common['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With'; */

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
