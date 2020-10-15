<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1 class="onboarding-sub-container-content-heading text-8xl introduction mb-8 text-center leading-none">
      Meet<br>your<br>lover
    </h1>
    <button class="onboarding-sub-container-content-button-outline w-1/2 mt-0" v-on:click="nextSlide()">
      {{slide.buttonText}}
    </button>
  </section>
</template>

<script>
export default {
  props: ['slide'],
  methods: {
    nextSlide() {
      this.$emit('next-slide');
    },
  },
};
</script>
