<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container relative">
    <h1 class="text-gray-matcha">{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none text-center">{{slide.header}}</h1>
    <ImageUpload v-if="imageIndex <= slide.maxImagesAllowed"
      v-bind:explanation="explanation"
      v-bind:bus="bus"
      v-on:imageUploaded="imageUploaded"
      v-on:imageDeleted="imageDeleted">
    </ImageUpload>
    <button class="onboarding-sub-container-slide-button"
            v-on:click="saveInput()">{{buttonText}}</button>
  </section>
</template>

<script>
/* eslint-disable */
import Vue from 'vue';
import ImageUpload from '@/components/app/onboarding/ImageUpload.vue';

export default {
  components: {
    ImageUpload,
  },
  props: ['slide'],
  data: () => ({
    imageIndex: 1,
    imagesUploaded: [],
    bus: new Vue(),
  }),
  methods: {
    imageUploaded(...args) {
      const [imageObject] = args;
      this.imagesUploaded.push(imageObject);
    },
    imageDeleted() {
      this.imagesUploaded.pop();
    },
    saveInput() {
      if (this.imagesUploaded.length === this.imageIndex && this.imageIndex !== this.slide.maxImagesAllowed) {
        this.bus.$emit('clearForNextImage');
        this.imageIndex += 1;
      } else {
        this.$emit('saveInput', this.slide.key, this.imagesUploaded);
      }
    },
  },
  computed: {
    explanation() {
      if (this.imageIndex === 1) {
        return this.slide.mainImageExplanation;
      }
      return `${this.slide.secondaryImageExplanation} ${this.imageIndex - 1} / ${this.slide.maxImagesAllowed - 1}`;
    },
    buttonText() {
      if (this.imagesUploaded.length === this.imageIndex) {
        return 'Continue';
      }
      return 'Skip';
    },
  },
};
</script>
