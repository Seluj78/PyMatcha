<template>
  <!-- eslint-disable max-len -->
  <button v-if="showScroll"
          class="z-10 fixed text-2xl text-white-matcha font-bold bottom-0 mx-auto ml-4 sm:ml-8 mb-8 w-12 h-12 rounded-full bg-purple-matcha"
          v-on:click="scrollUp()">
    ↑</button>
</template>

<script>
export default {
  data: () => ({
    showScroll: false,
  }),
  methods: {
    scrollUp() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    },
    handleScroll() {
      this.showScroll = window.scrollY > window.screen.height;
    },
  },
  created() {
    window.addEventListener('scroll', this.handleScroll);
  },
  destroyed() {
    window.removeEventListener('scroll', this.handleScroll);
  },
};
</script>
