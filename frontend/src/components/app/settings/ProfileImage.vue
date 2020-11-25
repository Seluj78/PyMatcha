<template>
<!--  eslint-disable max-len-->
  <div class="mt-4 max-w-2xl mx-auto">
    <div class="relative overflow-hidden bg-transparent rounded-md w-full" style="padding-bottom: 70%">
      <img v-bind:src="image.link" class="absolute object-cover w-full h-full rounded-md">
      <div class="absolute top-0 left-0 z-20 m-5">
        <img src="../../../assets/dots.png" v-on:click="showImageSettings = !showImageSettings " class="outline-none cursor-pointer h-3">
        <div v-if="showImageSettings" class="z-30 mt-4">
          <h1 class="text-red-500 text-center bg-white-matcha px-4 py-2 cursor-pointer rounded-md" v-on:click="deleteImage(image.id)">Delete</h1>
          <h1 class="text-green-500 text-center bg-white-matcha px-4 py-2 mt-2 cursor-pointer rounded-md" v-if="!image.is_primary" v-on:click="makePrimaryImage(image.id)">Make primary</h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['image'],
  data: () => ({
    showImageSettings: false,
  }),
  methods: {
    async deleteImage(imageId) {
      this.showImageSettings = false;
      this.$emit('delete-image', imageId);
    },
    async makePrimaryImage(imageId) {
      this.showImageSettings = false;
      this.$emit('make-primary-image', imageId);
    },
  },
};
</script>
