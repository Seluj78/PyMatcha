<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
    <div class="auth-sub-container-error mb-4" v-if="error.happened">
      <h1 class="auth-sub-container-error-message">{{error.message}}</h1>
    </div>
    <div class="auth-sub-container">
      <div class="auth-sub-container-content" v-if="!forgotPasswordEmailSent">
        <img src="../../assets/auth/lock.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Forgot password?</h1>
        <h1 class="text-sm text-gray-matcha text-center">Enter your email and we will send you a link, so you can log in again</h1>
      </div>
      <div class="auth-sub-container-content mt-4 w-full" v-if="!forgotPasswordEmailSent">
        <ValidationObserver v-slot="{ handleSubmit, invalid }" class="w-full">
          <form @submit.prevent="handleSubmit(onSubmit)">
            <ValidationProvider name="Email" rules="required|email|max:50" v-slot="{errors}">
              <input type="email" placeholder="Email" v-model="formData.email" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <input v-if="!submitted" type="submit" :disabled="invalid" value="Send reset link" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
            <div v-else class="flex items-center justify-center mt-4">
              <img class="h-12" src="../../assets/loading.svg">
            </div>
          </form>
        </ValidationObserver>
      </div>
      <div class="auth-sub-container-content" v-if="forgotPasswordEmailSent">
        <img src="../../assets/auth/email.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Check your email</h1>
        <h1 class="auth-sub-container-content-paragraph">Reset password link sent to {{formData.email}}</h1>
      </div>
    </div>
    <div class="auth-sub-container-thinner mt-4">
      <div class="auth-sub-container-content">
        <router-link to="/accounts/signin" class="auth-sub-container-content-link">Back to signing in</router-link>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data: () => ({
    formData: {
      email: '',
    },
    forgotPasswordEmailSent: false,
    error: {
      happened: false,
      message: '',
    },
    submitted: false,
  }),
  methods: {
    async onSubmit() {
      try {
        this.submitted = true;
        this.clearError();
        await this.sendResetPasswordLink();
        this.forgotPasswordEmailSent = true;
        this.submitted = false;
      } catch (error) {
        this.displayError(this.$errorMessenger(error));
        this.submitted = false;
      }
    },
    async sendResetPasswordLink() {
      await this.$http.post('/auth/password/forgot', this.formData);
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
