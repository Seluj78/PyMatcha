<template>
  <!-- eslint-disable max-len -->
  <!-- eslint-disable vue/no-deprecated-v-on-native-modifier -->
  <nav class="sm:flex sm:justify-between sm:items-center sm:py-5">
    <div class="flex items-center justify-between px-5 py-3 sm:p-0">
      <div id="logo">
        <router-link to="/">
          <div class="flex justify-center items-center">
            <img src="../../assets/logo.png" class="h-10">
            <h1 class="text-purple-matcha text-2xl font-bold ml-2">Matcha</h1>
          </div>
        </router-link>
      </div>
      <div id="burger" class="sm:hidden">
        <button type="button" class="block text-gray-800 focus:outline-none" v-on:click="isOpen = !isOpen">
          <svg class="w-8 h-8 text-purple-matcha fill-current" viewBox="0 0 24 24">
            <path v-if="!isOpen" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
            <path v-if="isOpen" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
          </svg>
        </button>
      </div>
    </div>
    <div id="links" v-on:click="isOpen = !isOpen" v-bind:class="isOpen ? 'block' : 'hidden'" class="px-2 pb-5 text-center sm:p-0 sm:block sm:flex sm:items-center">
      <div class="sm:flex sm:bg-purple-matcha sm:border-2 sm:border-purple-matcha sm:rounded-lg">
        <router-link v-if="!loggedIn" to="/accounts/signin" class="navigation-button-logged-in sm:hover:bg-white-matcha sm:hover:text-purple-matcha sm:text-purple-matcha sm:bg-white-matcha sm:py-2 sm:px-8 sm:rounded-md">Sign In</router-link>
        <router-link v-if="!loggedIn" to="/accounts/signup" class="navigation-button-logged-in sm:hover:bg-purple-matcha sm:hover:text-white-matcha sm:text-white-matcha sm:py-2 sm:px-8">Get Started</router-link>
      </div>
      <router-link v-if="loggedIn" to="/search" class="navigation-button-logged-in">Search</router-link>
      <router-link v-if="loggedIn" to="/add" class="navigation-button-logged-in">Add</router-link>
      <router-link v-if="loggedIn" v-on:click.native="logout()" to="/" class="navigation-button-logged-in">Log Out</router-link>
    </div>
  </nav>
</template>

<script>

/* eslint-disable indent */
export default {
  name: 'Navigation',
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    loggedIn() {
      return false;
    },
  },
  methods: {
    async logout() {
      return true;
    },
  },
};
</script>
