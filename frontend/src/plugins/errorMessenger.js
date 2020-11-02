import Vue from 'vue';

export default {
  install() {
    Vue.prototype.$errorMessenger = (error) => {
      if (error.response && error.response.status === 404) {
        return 'Something went wrong on our end. We will fix it soon. Please, try again later';
      }
      return error.response.data.error.message;
    };
  },
};
