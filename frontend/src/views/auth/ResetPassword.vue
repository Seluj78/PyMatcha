<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container" v-if="tokenIsValid">
    <div class="auth-sub-container-error" v-if="error.happened">
      <h1 class="auth-sub-container-error-message">{{error.message}}</h1>
    </div>
    <div class="auth-sub-container-thinner mt-4" v-if="error.happened">
      <div class="auth-sub-container-content">
        <h1 class="auth-sub-container-content-paragraph"><router-link to="/accounts/signin" class="auth-sub-container-content-link">Sign in</router-link></h1>
      </div>
    </div>
    <div class="auth-sub-container" v-if="!error.happened">
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
            <ValidationProvider name="Repeat Password" rules="required|confirmed:Password" v-slot="{errors}">
              <input type="password" placeholder="Repeat Password" v-model="formData.passwordRepeat" class="matcha-input mt-4">
              <span class="matcha-input-error">{{ passwordErrorHandler(errors[0]) }}</span>
            </ValidationProvider>
            <input v-if="!submitted" type="submit" :disabled="invalid" value="Reset password" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
            <div v-else class="flex items-center justify-center mt-4">
              <img class="h-12" src="../../assets/loading.svg">
            </div>
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
  async created() {
    await this.checkToken();
    this.tokenIsValid = true;
  },
  data: () => ({
    tokenIsValid: false,
    formData: {
      password: '',
      passwordRepeat: '',
    },
    passwordHasBeenReset: false,
    error: {
      happened: false,
      message: '',
    },
    submitted: false,
  }),
  methods: {
    passwordErrorHandler(error) {
      if (!error || error === 'The Password field is required' || error === 'The Repeat Password field is required') {
        return error;
      }
      if (error === 'The Repeat Password field confirmation does not match') {
        return 'Passwords do not match';
      }
      return 'This password is too easy to guess';
    },
    async onSubmit() {
      try {
        this.submitted = true;
        this.clearError();
        await this.resetPassword();
        this.passwordHasBeenReset = true;
        this.submitted = false;
      } catch (error) {
        this.displayError(this.$errorMessenger(error));
        this.submitted = false;
      }
    },
    async checkToken() {
      try {
        const { token } = this.$route.query;
        if (!token) {
          await this.$router.push('/accounts/password/reseterror');
          return;
        }
        await this.$http.post('/auth/password/check_token', { token });
      } catch (error) {
        await this.$router.push('/accounts/password/reseterror');
      }
    },
    async resetPassword() {
      const { password } = this.formData;
      const { token } = this.$route.query;
      await this.$http.post('/auth/password/reset', { password, token });
    },
    clearError() {
      this.error.message = '';
      this.error.happened = false;
    },
    displayError(message) {
      this.error.message = message;
      this.error.happened = true;
    },
  },
};

</script>
