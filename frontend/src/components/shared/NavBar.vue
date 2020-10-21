<template>
  <!-- eslint-disable max-len -->
  <!-- eslint-disable vue/no-deprecated-v-on-native-modifier -->
  <nav class="sm:flex sm:justify-between sm:items-center sm:py-5">
    <div class="flex items-center justify-between px-5 py-3 sm:p-0">
      <div id="logo">
        <router-link to="/">
          <div class="flex justify-center items-center">
            <img src="../../assets/logo.png" class="h-6">
            <h1 v-if="!loggedIn" class="text-purple-matcha text-xl ml-2">Matcha</h1>
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
      <div v-if="!loggedIn" class="sm:flex sm:bg-purple-matcha sm:border-2 sm:border-purple-matcha sm:rounded-lg">
        <router-link to="/accounts/signin" class="navigation-button-logged-in sm:hover:bg-white-matcha sm:hover:text-purple-matcha sm:text-purple-matcha sm:bg-white-matcha sm:py-2 sm:px-8 sm:rounded-md">Sign In</router-link>
        <router-link to="/accounts/signup" class="navigation-button-logged-in sm:hover:bg-purple-matcha sm:hover:text-white-matcha sm:text-white-matcha sm:py-2 sm:px-8">Get Started</router-link>
      </div>
      <router-link v-if="loggedIn" to="/browse" v-bind:class="{'navigation-button-logged-in': true, 'bg-purple-matcha': currentRoute === 'Browse', 'text-white-matcha': currentRoute === 'Browse'}">Browse</router-link>
      <router-link v-if="loggedIn" to="/search" v-bind:class="{'navigation-button-logged-in': true, 'bg-purple-matcha': currentRoute === 'Search', 'text-white-matcha': currentRoute === 'Search'}">Search</router-link>
      <router-link v-if="loggedIn" to="/matches" v-bind:class="{'navigation-button-logged-in': true, 'bg-purple-matcha': currentRoute === 'Matches', 'text-white-matcha': currentRoute === 'Matches'}" class="navigation-button-logged-in">Matches</router-link>
      <router-link v-if="loggedIn" to="/settings" v-bind:class="{'navigation-button-logged-in': true, 'bg-purple-matcha': currentRoute === 'Settings', 'text-white-matcha': currentRoute === 'Settings'}">Settings</router-link>
      <router-link v-if="loggedIn" to="/history" v-bind:class="{'navigation-button-logged-in': true, 'bg-purple-matcha': currentRoute === 'History', 'text-white-matcha': currentRoute === 'History'}">History</router-link>
      <router-link v-if="loggedIn" v-on:click.native="logout()" to="/" class="navigation-button-logged-in">Exit</router-link>
    </div>
  </nav>
</template>

<script>
/* eslint-disable indent */
import { logOut } from '@/auth/logOut';

export default {
  name: 'Navigation',
  props: ['currentRoute'],
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    loggedIn() {
      return this.$store.getters.getLoggedInUser;
    },
  },
  methods: {
    async logout() {
      await logOut();
    },
  },
};
</script>
