<template>
  <!-- eslint-disable max-len -->
  <div class="w-full max-w-sm flex flex-col justify-center items-center">
    <div class="w-full mt-4">
      <p class="text-gray-matcha text-center">{{explanation}}</p>
    </div>
    <div class="auth-sub-container-error mt-8" v-if="image.error">
      <h1 class="auth-sub-container-error-message">{{image.error}}</h1>
    </div>
    <button v-if="!image.uploaded" class="overflow-hidden relative onboarding-sub-container-upload-button w-full my-8">
      <input style="padding-left: 100%;" class="cursor-pointer opacity-0 absolute top-0 left-0 w-full h-full rounded-md" type="file" v-on:change="selectFile()" ref="file">
      <img src="../../../assets/onboarding/cloud.png" class="w-8 mx-auto">
    </button>
    <div v-if="image.uploaded" class="relative overflow-hidden bg-transparent rounded-md w-full my-10" style="padding-bottom: 70%">
      <img src="../../../assets/onboarding/remove.png" class="absolute cursor-pointer top-0 right-0  w-8 z-10" v-on:click="deleteImage()">
      <img v-bind:src="image.url" class="absolute object-cover w-full h-full rounded-md">
    </div>
  </div>
</template>

<script>
/* eslint-disable */

export default {
  props: ['explanation', 'bus'],
  data: () => ({
    image: {
      uploaded: false,
      url: null,
      content: null,
      error: null,
    },
  }),
  methods: {
    selectFile() {
      this.image.error = '';
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const file = this.$refs.file.files[0];

      if (!allowedTypes.includes(file.type)) {
        this.image.error = 'Only images allowed';
        return;
      }
      if (file.size > 2000000) {
        this.image.error = 'File too large';
        return;
      }
      this.image.content = file;
      this.image.url = URL.createObjectURL(file);
      this.image.uploaded = true;
      this.$emit('imageUploaded', {
        'content' : this.image.content,
        'url' : this.image.url,
      });
    },
    deleteImage() {
      this.clearForNextImage();
      this.$emit('imageDeleted');
    },
    clearForNextImage() {
      this.image.uploaded = false;
      this.image.url = null;
      this.image.content = null;
      this.image.error = null;
    },
  },
  mounted() {
    this.bus.$on('clearForNextImage', this.clearForNextImage);
  },
};
</script>
