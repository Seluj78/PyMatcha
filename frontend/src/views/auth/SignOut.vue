<template>
  <div>signing out...</div>
</template>

<script>

/* eslint-disable no-empty */

export default {
  name: 'SignOut',
  async mounted() {
    try {
      await this.$http.post('/auth/logout', {
        access_token: localStorage.getItem(process.env.VUE_APP_ACCESS_TOKEN),
        refresh_token: localStorage.getItem(process.env.VUE_APP_REFRESH_TOKEN),
      });
    } catch (e) {}
    localStorage.removeItem(process.env.VUE_APP_ACCESS_TOKEN);
    localStorage.removeItem(process.env.VUE_APP_REFRESH_TOKEN);
    localStorage.removeItem(process.env.VUE_APP_VUEX_PERSISTED_STATE);
    localStorage.removeItem(process.env.VUE_APP_SECURE_LS_METADATA);
    await this.$store.dispatch('logout');
    window.location.reload();
  },
};
</script>
