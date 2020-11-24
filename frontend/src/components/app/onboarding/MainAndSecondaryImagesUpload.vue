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
        this.$emit('next-slide');
        this.sendImagesToBackend();
      }
    },
    async sendImagesToBackend() {
      for (let i = 0; i < this.imagesUploaded.length; i += 1) {
        try {
          const formData = new FormData();
          formData.append('file[]', this.imagesUploaded[i].content);
          if (i === 0) {
            await this.$http.post('/profile/images?is_primary=true', formData, { accessTokenRequired: true });
          } else {
            await this.$http.post('/profile/images?is_primary=false', formData, { accessTokenRequired: true });
          }
        } catch (error) {}
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
      if (this.imageIndex === 1) {
        return 'Skip';
      }
      return 'No more';
    },
  },
};
</script>
