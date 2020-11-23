<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
    <div class="auth-sub-container-error mb-4" v-if="error.happened">
      <h1 class="auth-sub-container-error-message">{{error.message}}</h1>
    </div>
    <div class="auth-sub-container">
      <div class="auth-sub-container-content">
        <div class="flex">
          <img src="../../assets/logo.png" class="h-12">
          <h1 class="text-purple-matcha text-4xl font-bold ml-2">Matcha</h1>
        </div>
      </div>
      <div class="auth-sub-container-content mt-4">
        <ValidationObserver v-slot="{ handleSubmit, invalid }">
          <form @submit.prevent="handleSubmit(onSubmit)">
            <ValidationProvider name="Username" rules="required|max:100" v-slot="{errors}">
              <input type="text" placeholder="Username" v-model="formData.username" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <ValidationProvider name="Password" rules="required|max:100" v-slot="{errors}">
              <input type="password" placeholder="Password" v-model="formData.password" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <input v-if="!submitted" type="submit" :disabled="invalid" value="Sign In" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
            <div v-else class="flex items-center justify-center mt-4">
              <img class="h-12" src="../../assets/loading.svg">
            </div>
          </form>
        </ValidationObserver>
      </div>
      <hr class="bg-gray-300 w-full my-4">
      <div class="auth-sub-container-content">
        <router-link to="/accounts/password/forgot" class="auth-sub-container-content-link">Forgot password?</router-link>
      </div>
    </div>
    <div class="auth-sub-container-thinner mt-4">
      <div class="auth-sub-container-content">
        <h1 class="auth-sub-container-content-paragraph">Don't have an account? <router-link to="/accounts/signup" class="auth-sub-container-content-link">Sign up</router-link></h1>
      </div>
    </div>
  </div>
</template>

<script>
import jwtDecode from 'jwt-decode';

export default {
  data: () => ({
    formData: {
      username: '',
      password: '',
    },
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
        const response = await this.signInUser(this.formData);
        localStorage.setItem(process.env.VUE_APP_ACCESS_TOKEN, response.data.return.access_token);
        localStorage.setItem(process.env.VUE_APP_REFRESH_TOKEN, response.data.return.refresh_token);
        const userId = this.getUserFromJwt(response.data.return.access_token).id;
        const user = await this.$http.get(`/users/${userId}`, { accessTokenRequired: true });
        await this.$store.dispatch('login', user.data);
        if (response.data.return.is_profile_completed) {
          this.$router.push('/browse');
        } else {
          this.$router.push('/onboarding');
        }
        this.submitted = false;
      } catch (error) {
        this.displayError(this.$errorMessenger(error));
        this.submitted = false;
      }
    },
    async signInUser(user) {
      const response = await this.$http.post('/auth/login', user);
      return response;
    },
    getUserFromJwt(token) {
      const { identity } = jwtDecode(token);
      return identity;
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
