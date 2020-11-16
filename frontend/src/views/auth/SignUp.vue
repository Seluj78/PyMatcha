<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
    <div class="auth-sub-container-error mb-4" v-if="error.happened">
      <h1 class="auth-sub-container-error-message">{{error.message}}</h1>
    </div>
    <div class="auth-sub-container">
      <div class="auth-sub-container-content" v-if="!confirmationEmailSent">
        <div class="flex justify-center items-center">
          <img src="../../assets/logo.png" class="h-10">
          <h1 class="text-purple-matcha text-4xl font-bold ml-2">Matcha</h1>
        </div>
        <h1 class="auth-sub-container-content-heading my-0">Find your significant other</h1>
      </div>
      <div class="auth-sub-container-content" v-if="!confirmationEmailSent">
        <ValidationObserver v-slot="{ handleSubmit, invalid }">
          <form @submit.prevent="handleSubmit(onSubmit)" class="mt-4">
            <ValidationProvider name="First Name" rules="required|alpha|max:20" v-slot="{errors}">
              <input type="text" placeholder="First Name" v-model="formData.first_name" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <ValidationProvider name="Last Name" rules="required|alpha|max:20" v-slot="{errors}">
              <input type="text" placeholder="Last Name" v-model="formData.last_name" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <ValidationProvider name="Email" rules="required|email|max:50" v-slot="{errors}">
              <input type="email" placeholder="Email" v-model="formData.email" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <ValidationProvider name="Username" rules="required|alpha_dash|max:20" v-slot="{errors}">
              <input type="text" placeholder="Username" v-model="formData.username" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <ValidationProvider name="Password" rules="required|min:6|validPassword" v-slot="{errors}">
              <input type="password" placeholder="Password" v-model="formData.password" class="matcha-input">
              <span class="matcha-input-error">{{ passwordErrorHandler(errors[0]) }}</span>
            </ValidationProvider>
            <input v-if="!submitted" type="submit" :disabled="invalid" value="Sign Up" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
            <div v-else class="flex items-center justify-center mt-4">
              <img class="h-12" src="../../assets/loading.svg">
            </div>
          </form>
        </ValidationObserver>
      </div>
      <div class="auth-sub-container-content" v-if="confirmationEmailSent">
        <img src="../../assets/auth/email.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Verify your email</h1>
        <h1 class="auth-sub-container-content-paragraph">Click confirmation link sent to {{formData.email}}</h1>
      </div>
    </div>
    <div v-if="!confirmationEmailSent" class="auth-sub-container-thinner mt-4">
      <div class="auth-sub-container-content">
        <h1 class="auth-sub-container-content-paragraph">Have an account? <router-link to="/accounts/signin" class="auth-sub-container-content-link">Sign in</router-link></h1>
      </div>
    </div>
    <div v-else class="auth-sub-container-thinner mt-4">
      <div class="auth-sub-container-content">
        <h1 class="auth-sub-container-content-paragraph">Already verified? <router-link to="/accounts/signin" class="auth-sub-container-content-link">Sign in</router-link></h1>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data: () => ({
    formData: {
      first_name: '',
      last_name: '',
      email: '',
      username: '',
      password: '',
    },
    confirmationEmailSent: false,
    error: {
      happened: false,
      message: '',
    },
    submitted: false,
  }),
  methods: {
    passwordErrorHandler(error) {
      if (!error || error === 'The Password field is required') {
        return error;
      }
      return 'This password is too easy to guess';
    },
    async onSubmit() {
      try {
        this.submitted = true;
        this.clearError();
        await this.signUpUser(this.formData);
        this.confirmationEmailSent = true;
        this.submitted = false;
      } catch (error) {
        this.displayError(this.$errorMessenger(error));
        this.submitted = false;
      }
    },
    async signUpUser(user) {
      await this.$http.post('/auth/register', user);
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
