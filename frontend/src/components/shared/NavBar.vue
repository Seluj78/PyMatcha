<template>
  <!-- eslint-disable max-len -->
  <!-- eslint-disable vue/no-deprecated-v-on-native-modifier -->
  <nav v-if="showNavigationBar" class="md:flex md:justify-between md:items-center md:py-5">
    <div class="flex items-center justify-between px-5 py-3 md:p-0 w-full">
      <div id="logo">
        <router-link to="/">
          <div class="flex justify-center items-center">
            <img src="../../assets/logo.png" class="h-6">
            <h1 v-if="!loggedIn" class="text-purple-matcha text-xl ml-2">Matcha</h1>
          </div>
        </router-link>
      </div>
      <NavBarBell v-if="loggedIn"></NavBarBell>
      <div id="burger" class="md:hidden">
        <button type="button" class="block text-gray-800 focus:outline-none" v-on:click="isOpen = !isOpen">
          <svg class="w-8 h-8 text-purple-matcha fill-current" viewBox="0 0 24 24">
            <path v-if="!isOpen" fill-rule="evenodd" d="M4 5h16a1 1 0 0 1 0 2H4a1 1 0 1 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2zm0 6h16a1 1 0 0 1 0 2H4a1 1 0 0 1 0-2z"/>
            <path v-if="isOpen" fill-rule="evenodd" d="M18.278 16.864a1 1 0 0 1-1.414 1.414l-4.829-4.828-4.828 4.828a1 1 0 0 1-1.414-1.414l4.828-4.829-4.828-4.828a1 1 0 0 1 1.414-1.414l4.829 4.828 4.828-4.828a1 1 0 1 1 1.414 1.414l-4.828 4.829 4.828 4.828z"/>
          </svg>
        </button>
      </div>
    </div>
    <div id="links" v-on:click="openOnSmallerScreens()" v-bind:class="isOpen ? 'block' : 'hidden'" class="px-2 pb-5 text-center md:p-0 md:block md:flex md:items-center">
      <div v-if="!loggedIn" class="md:flex md:bg-purple-matcha md:border-2 md:border-purple-matcha md:rounded-lg">
        <router-link to="/accounts/signin" class="navigation-button-logged-in md:hover:bg-white-matcha md:hover:text-purple-matcha md:text-purple-matcha md:bg-white-matcha md:py-2 md:px-8 md:rounded-md mx-0">Sign In</router-link>
        <router-link to="/accounts/signup" class="navigation-button-logged-in md:hover:bg-purple-matcha md:hover:text-white-matcha md:text-white-matcha md:py-2 md:px-8">Get Started</router-link>
      </div>
      <router-link v-if="loggedIn" to="/browse" v-bind:class="{'navigation-button-logged-in': true, 'font-black': currentRoute === 'Browse'}">Browse</router-link>
      <router-link v-if="loggedIn" to="/search" v-bind:class="{'navigation-button-logged-in': true, 'font-black': currentRoute === 'Search'}">Search</router-link>
      <router-link v-if="loggedIn" to="/matches" v-bind:class="{'navigation-button-logged-in': true, 'font-black': currentRoute === 'Matches'}">Matches</router-link>
      <router-link v-if="loggedIn" to="/settings" v-bind:class="{'navigation-button-logged-in': true, 'font-black': currentRoute === 'Settings'}">Settings</router-link>
      <router-link v-if="loggedIn" to="/history" v-bind:class="{'navigation-button-logged-in': true, 'font-black': currentRoute === 'History'}">History</router-link>
      <router-link v-if="loggedIn" to="/accounts/signout" class="navigation-button-logged-in">Exit</router-link>
    </div>
  </nav>
</template>

<script>
/* eslint-disable indent */

import NavBarBell from '@/components/shared/NavBarBell.vue';

export default {
  name: 'Navigation',
  components: {
    NavBarBell,
  },
  data() {
    return {
      isOpen: false,
      route: null,
      dontShowOn: [
        'SignUp',
        'SignIn',
        'ForgotPassword',
        'ResetPassword',
        'ResetPasswordError',
        'AccountVerified',
        'AccountVerifiedError',
        'Onboarding',
        'SignOut',
      ],
    };
  },
  methods: {
    openOnSmallerScreens() {
      if (window.innerWidth <= 768) {
        this.isOpen = !this.isOpen;
      }
    },
  },
  watch: {
    $route(to) {
      this.route = to.name;
    },
  },
  computed: {
    loggedIn() {
      return this.$store.getters.getLoggedInUser;
    },
    currentRoute() {
      return this.route;
    },
    showNavigationBar() {
      return this.dontShowOn.indexOf(this.route) === -1;
    },
  },
  beforeMount() {
    this.route = this.$router.currentRoute.name;
  },
};
</script>
