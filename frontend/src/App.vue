<template>
  <div id="app" class="antialiased" v-bind:style="{background: getBackground}">
    <NavBar class="px-4 sm:px-16 lg:px-32"></NavBar>
    <keep-alive include="Browse,Search,History">
      <router-view/>
    </keep-alive>
  </div>
</template>

<script>

import NavBar from '@/components/shared/NavBar.vue';

export default {
  components: {
    NavBar,
  },
  computed: {
    getBackground() {
      const currentRoute = this.$route.name;
      if (currentRoute === 'Onboarding') {
        return '#FDFDFD';
      }
      return '#FFFFFE';
    },
  },
};
</script>

<style>
html {
  @apply bg-white-matcha;
}
html,
body,
#app {
  height: 100%;
}

body {
  margin: 0;
}

::placeholder {
  @apply font-normal;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active  {
  -webkit-box-shadow: 0 0 0 30px #FFFFFE inset !important;
}

input:-webkit-autofill {
  -webkit-text-fill-color: #2d3748 !important;
}

.noSelect {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

</style>
