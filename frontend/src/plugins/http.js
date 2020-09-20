import Axios from 'axios';
import Vue from 'vue';

function createAxiosInstance(baseURL) {
  return Axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.token}`,
    },
  });
}

const axiosInstance = createAxiosInstance(process.env.VUE_APP_BACKEND_BASE_URL);

export default {
  install() {
    Vue.prototype.$http = axiosInstance;
  },
};
