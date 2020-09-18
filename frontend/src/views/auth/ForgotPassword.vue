<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
    <div class="auth-sub-container">
      <div class="auth-sub-container-content" v-if="!resetPasswordEmailSent">
        <img src="../../assets/auth/lock.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Forgot password?</h1>
        <h1 class="text-sm text-gray-matcha text-center">Enter your email and we will send you a link, so you can log in again</h1>
      </div>
      <div class="auth-sub-container-content mt-4" v-if="!resetPasswordEmailSent">
        <ValidationObserver v-slot="{ handleSubmit, invalid }">
          <form @submit.prevent="handleSubmit(onSubmit)">
            <ValidationProvider name="Email" rules="required|email|max:50" v-slot="{errors}">
              <input type="email" placeholder="Email" v-model="formData.email" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <input type="submit" :disabled="invalid" value="Reset password" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
          </form>
        </ValidationObserver>
      </div>
      <div class="auth-sub-container-content" v-if="resetPasswordEmailSent">
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
    resetPasswordEmailSent: false,
  }),
  methods: {
    onSubmit() {
      this.resetPasswordEmailSent = true;
    },
  },
};

</script>
