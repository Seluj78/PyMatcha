<template>
  <!-- eslint-disable max-len -->
  <div class="w-full max-w-sm flex flex-col justify-center items-center">
    <div class="w-full mt-4">
      <p class="text-gray-matcha text-center">{{info.explanation}}</p>
    </div>
    <button v-if="!image.uploaded" class="relative onboarding-sub-container-upload-button w-full my-8">
      <input class="cursor-pointer opacity-0 absolute top-0 left-0 w-full h-full rounded-md" type="file" v-on:change="selectFile()" ref="file">
      <img src="../../../assets/onboarding/cloud.png" class="w-8 mx-auto">
    </button>
    <div v-if="image.uploaded" class="relative overflow-hidden bg-transparent rounded-md w-full my-10" style="padding-bottom: 70%">
      <img src="../../../assets/onboarding/remove.png" class="absolute cursor-pointer top-0 right-0  w-8 z-10" v-on:click="deleteImage()">
      <img v-bind:src="image.url" class="absolute object-cover w-full h-full rounded-md">
    </div>
  </div>
</template>

<script>
export default {
  props: ['info', 'bus'],
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
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const file = this.$refs.file.files[0];
      this.image.content = file;

      if (!allowedTypes.includes(file.type)) {
        this.image.error = 'Only images allowed';
        return;
      }
      if (file.size > 2000000) {
        this.image.error = 'File too large';
        return;
      }
      this.image.url = URL.createObjectURL(file);
      this.image.uploaded = true;
      this.$emit('imageUploaded');
    },
    deleteImage() {
      this.image.uploaded = false;
      this.image.url = null;
      this.image.content = null;
      this.image.error = null;
      this.$emit('imageDeleted');
    },
    getImageObject() {
      this.$emit('imageObjectGiven', this.image);
      this.deleteImage();
    },
  },
  mounted() {
    this.bus.$on('getImageObject', this.getImageObject);
  },
};
</script>
