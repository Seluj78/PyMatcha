<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
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
            <ValidationProvider name="Username" rules="required|max:20" v-slot="{errors}">
              <input type="text" placeholder="Username" v-model="formData.username" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <ValidationProvider name="Password" rules="required|max:100" v-slot="{errors}">
              <input type="password" placeholder="Password" v-model="formData.password" class="matcha-input">
              <span class="matcha-input-error">{{ errors[0] }}</span>
            </ValidationProvider>
            <input type="submit" :disabled="invalid" value="Sign In" v-bind:class="{'auth-sub-container-content-submit-button': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
          </form>
        </ValidationObserver>
      </div>
      <hr class="bg-gray-300 w-full my-4">
      <div class="auth-sub-container-content">
        <router-link to="/accounts/password/reset" class="auth-sub-container-content-link">Forgot password?</router-link>
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

export default {
  data: () => ({
    formData: {
      username: '',
      password: '',
    },
  }),
  methods: {
    onSubmit() {
      console.log('nice');
    },
  },
};

</script>
