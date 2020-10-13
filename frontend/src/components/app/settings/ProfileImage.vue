<template>
<!--  eslint-disable max-len-->
  <div class="mt-4">
    <div class="relative overflow-hidden bg-transparent rounded-md w-full" style="padding-bottom: 70%">
      <img v-bind:src="image.link" class="absolute object-cover w-full h-full rounded-md">
      <div class="absolute top-0 left-0 z-20 m-5">
        <img src="../../../assets/dots.png" tabindex="2" @focusout="showImageSettings = false" v-on:click="showImageSettings = !showImageSettings " class="outline-none cursor-pointer h-3">
        <div v-if="showImageSettings" class="z-30 mt-4">
          <h1 class="text-white-matcha font-bold text-center bg-red-500 px-4 py-2 cursor-pointer rounded-md" v-on:click="deleteImage(image.id)">Delete</h1>
          <h1 class="text-white-matcha font-bold text-center bg-green-500 px-4 py-2 mt-2 cursor-pointer rounded-md" v-if="!image.is_primary" v-on:click="makePrimaryImage(image.id)">Make primary</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable  vue/custom-event-name-casing */
export default {
  props: ['image'],
  data: () => ({
    showImageSettings: false,
  }),
  methods: {
    async deleteImage(imageId) {
      this.showImageSettings = false;
      this.$emit('deleteImage', imageId);
    },
    async makePrimaryImage(imageId) {
      this.showImageSettings = false;
      this.$emit('makePrimaryImage', imageId);
    },
  },
};
</script>
