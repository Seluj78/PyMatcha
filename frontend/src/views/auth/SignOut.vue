<template>
  <section class="mx-auto onboarding-sub-container bg-white w-full h-screen relative">
    <h1
      class="onboarding-sub-container-content-heading text-5xl mx-auto leading-none text-center">
      Signing<br>out
    </h1>
    <img class="mt-4 h-32 mx-auto" src='../../assets/loading.svg'>
  </section>
</template>

<script>

export default {
  name: 'SignOut',
  async mounted() {
    await this.$http.post('/auth/logout', {
      access_token: localStorage.getItem(process.env.VUE_APP_ACCESS_TOKEN),
      refresh_token: localStorage.getItem(process.env.VUE_APP_REFRESH_TOKEN),
    });
    localStorage.removeItem(process.env.VUE_APP_ACCESS_TOKEN);
    localStorage.removeItem(process.env.VUE_APP_REFRESH_TOKEN);
    localStorage.removeItem(process.env.VUE_APP_VUEX_PERSISTED_STATE);
    localStorage.removeItem(process.env.VUE_APP_SECURE_LS_METADATA);
    await this.$store.dispatch('logout');
    window.location.reload();
  },
};
</script>
