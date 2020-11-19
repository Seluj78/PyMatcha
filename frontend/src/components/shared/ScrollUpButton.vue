<template>
  <!-- eslint-disable max-len -->
  <div class="fixed bottom-0 w-full flex justify-center left-0">
    <button v-if="showScroll"
            class="z-10 text-2xl text-white-matcha font-bold mb-10 w-12 h-12 rounded-full bg-purple-matcha"
            v-on:click="scrollUp()">
      ↑</button>
  </div>
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
