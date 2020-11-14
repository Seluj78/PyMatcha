<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container" v-if="verified">
    <div class="auth-sub-container">
      <div class="auth-sub-container-content">
        <img src="../../assets/auth/celebration.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">You are now verified</h1>
        <h1 class="text-sm text-gray-matcha text-center">Find interesting people, chat and set up dates. Someone is waiting for you.</h1>
        <router-link to="/accounts/signin" class="auth-sub-container-content-button">Sign in</router-link>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data: () => ({
    verified: false,
  }),
  async created() {
    try {
      await this.checkToken();
      await this.verifyUser();
      this.verified = true;
    } catch (error) {
      await this.$router.push('/accounts/verify/error');
    }
  },
  methods: {
    async checkToken() {
      const { token } = this.$route.query;
      if (!token) {
        throw new Error('Invalid token');
      }
    },
    async verifyUser() {
      const { token } = this.$route.query;
      await this.$http.post(`/auth/confirm/${token}`, {});
    },
  },
};

</script>
