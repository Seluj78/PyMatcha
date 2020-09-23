<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container relative">
    <h1>{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none text-center">Images</h1>
    <ImageUpload v-if="secondaryUpload === 0"
      v-bind:info="{explanation: 'Profile image'}"
      v-bind:bus="bus"
      v-on:imageObjectGiven="imageObjectGiven"
      v-on:imageUploaded="imageUploaded"
      v-on:imageDeleted="imageDeleted">
    </ImageUpload>
    <ImageUpload v-if="secondaryUpload === 1"
      v-bind:info="{explanation: `Extra image ${secondaryUpload} / ${secondaryMaxUpload}`}"
      v-bind:bus="bus"
      v-on:imageObjectGiven="imageObjectGiven"
      v-on:imageUploaded="imageUploaded"
      v-on:imageDeleted="imageDeleted">
    </ImageUpload>
    <ImageUpload v-if="secondaryUpload === 2"
      v-bind:info="{explanation: `Extra image ${secondaryUpload} / ${secondaryMaxUpload}`}"
      v-bind:bus="bus"
      v-on:imageObjectGiven="imageObjectGiven"
      v-on:imageUploaded="imageUploaded"
      v-on:imageDeleted="imageDeleted">
    </ImageUpload>
    <ImageUpload v-if="secondaryUpload === 3"
      v-bind:info="{explanation: `Extra image ${secondaryUpload} / ${secondaryMaxUpload}`}"
      v-bind:bus="bus"
      v-on:imageObjectGiven="imageObjectGiven"
      v-on:imageUploaded="imageUploaded"
      v-on:imageDeleted="imageDeleted">
    </ImageUpload>
    <ImageUpload v-if="secondaryUpload === 4"
      v-bind:info="{explanation: `Extra image ${secondaryUpload} / ${secondaryMaxUpload}`}"
      v-bind:bus="bus"
      v-on:imageObjectGiven="imageObjectGiven"
      v-on:imageUploaded="imageUploaded"
      v-on:imageDeleted="imageDeleted">
    </ImageUpload>
    <button class="onboarding-sub-container-content-button-outline-light mt-0"
            v-on:click="saveInput()">{{buttonText}}</button>
  </section>
</template>

<script>
import Vue from 'vue';
import ImageUpload from '@/components/app/onboarding/ImageUpload.vue';

export default {
  components: {
    ImageUpload,
  },
  props: ['slide'],
  data: () => ({
    secondaryUpload: 0,
    secondaryMaxUpload: 4,
    secondaryUploaded: [],
    buttonText: 'Skip',
    bus: new Vue(),
  }),
  methods: {
    imageUploaded() {
      this.buttonText = 'Continue';
    },
    imageDeleted() {
      this.buttonText = 'Skip';
    },
    saveInput() {
      this.bus.$emit('getImageObject');
    },
    imageObjectGiven(...args) {
      const [imageObject] = args;
      this.secondaryUploaded.push(imageObject);
      if (imageObject.url && this.secondaryUpload !== 4) {
        this.secondaryUpload += 1;
      } else {
        this.$emit('saveInput', 'slideFive', this.secondaryUploaded, 0);
      }
    },
    select(...args) {
      const [val] = args;
      this.optionSelected.push(val);
    },
  },
};
</script>
