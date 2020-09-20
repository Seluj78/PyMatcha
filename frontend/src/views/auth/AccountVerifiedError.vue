<template>
  <!-- eslint-disable max-len -->
  <div class="auth-container">
    <div class="auth-sub-container">
      <div class="auth-sub-container-content">
        <img src="../../assets/auth/error.png" class="h-12">
        <h1 class="auth-sub-container-content-heading">Something is wrong</h1>
        <h1 class="text-sm text-gray-matcha text-center">Either user has been verified already or this request is invalid</h1>
        <router-link to="/accounts/signin" class="auth-sub-container-content-link mt-4">Sign in</router-link>
      </div>
    </div>
    <div class="auth-sub-container-thinner mt-4">
      <div class="auth-sub-container-content">
        <router-link to="/accounts/signup" class="auth-sub-container-content-link">Sign up</router-link>
      </div>
    </div>
  </div>
</template>
