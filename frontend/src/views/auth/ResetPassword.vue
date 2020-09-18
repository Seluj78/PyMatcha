<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
    <div class="auth-sub-container-error mb-4" v-if="error.happened">
      <h1 class="auth-sub-container-error-message">{{error.message}}</h1>
    </div>
    <div class="auth-sub-container">
      <div class="auth-sub-container-content" v-if="!passwordHasBeenReset">
        <img src="../../assets/auth/refresh.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Enter your new password</h1>
      </div>
      <div class="auth-sub-container-content" v-if="!passwordHasBeenReset">
        <ValidationObserver v-slot="{ handleSubmit, invalid }">
          <form @submit.prevent="handleSubmit(onSubmit)">
            <ValidationProvider name="Password" rules="required|min:6|validPassword" v-slot="{errors}">
              <input type="password" placeholder="New Password" v-model="formData.password" class="matcha-input mt-0">
              <span class="matcha-input-error">{{ passwordErrorHandler(errors[0]) }}</span>
            </ValidationProvider>
            <input type="submit" :disabled="invalid" value="Reset password" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
          </form>
        </ValidationObserver>
      </div>
      <div class="auth-sub-container-content" v-if="passwordHasBeenReset">
        <img src="../../assets/auth/success.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Your password has been reset</h1>
        <router-link to="/accounts/signin" class="auth-sub-container-content-link">Sign in</router-link>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  async beforeMount() {
    await this.checkToken();
  },
  data: () => ({
    formData: {
      password: '',
    },
    passwordHasBeenReset: false,
    error: {
      happened: false,
      message: '',
    },
  }),
  methods: {
    passwordErrorHandler(error) {
      if (!error || error === 'The Password field is required') {
        return error;
      }
      return 'This password is too easy to guess';
    },
    async onSubmit() {
      const resetPasswordResponse = await this.$http.post('/auth/password/reset', this.formData);
      if (resetPasswordResponse.status !== 200) {
        this.error.message = resetPasswordResponse.data.error.message;
        this.error.happened = true;
        return;
      }
      this.passwordHasBeenReset = true;
    },
    async checkToken() {
      const { token } = this.$route.query;
      if (!token) {
        await this.$router.push('/accounts/password/reseterror');
        return;
      }
      const tokenCheck = await this.$http.post('/auth/password/check_token', { token });
      if (tokenCheck.status !== 200) {
        await this.$router.push('/accounts/password/reseterror');
      }
    },
  },
};

</script>
