<template>
  <div id="app" class="antialiased">
    <router-view/>
  </div>
</template>

<script>

export default {
  components: {
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

</style>
