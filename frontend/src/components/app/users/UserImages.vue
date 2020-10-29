<template>
  <div
    class="relative image-height"
    v-bind:style="{
      'background-repeat': 'no-repeat',
      'background-position': 'center center',
      'background-size' :'cover',
      'background-image': 'url(' + getImage() + ')'}">
    <div v-if="imagesCount > 1" class="absolute flex w-full top-0 left-0 w-full z-10 px-8 pt-1">
      <div v-for="image in this.images" :key="image.id"
           v-on:click="setImage(image.id)"
           v-bind:class="{
           'flex-1':true,
           'mx-2': true,
           'h-2': true,
           'rounded-md': true,
           'bg-gray-200': true,
           'cursor-pointer': image.id !== currentImage,
           'bg-gray-400': image.id === currentImage}"></div>
    </div>
    <div v-bind:class="{
      'absolute': true,
      'top-0': true,
      'left-0': true,
      'w-1/2': true,
      'h-full': true,
      'cursor-pointer': this.currentImage > 0}" v-on:click="prevImage()"></div>
    <div v-bind:class="{
      'absolute': true,
      'top-0': true,
      'right-0': true,
      'w-1/2': true,
      'h-full': true,
      'cursor-pointer': this.currentImage < this.imagesCount - 1}" v-on:click="nextImage()"></div>
  </div>
</template>

<script>
import imageMan from '../../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../../assets/recommendations/avatars/other.png';

export default {
  props: ['images', 'gender'],
  data: () => ({
    currentImage: 0,
    imagesCount: 0,
  }),
  methods: {
    nextImage() {
      if (this.currentImage < this.imagesCount - 1) {
        this.currentImage += 1;
      }
    },
    prevImage() {
      if (this.currentImage > 0) {
        this.currentImage -= 1;
      }
    },
    setImage(index) {
      this.currentImage = index;
    },
    getImage() {
      if (this.images.length) {
        return this.images[this.currentImage].link;
      }
      if (this.gender === 'male') {
        return imageMan;
      }
      if (this.gender === 'female') {
        return imageWoman;
      }
      return imageOther;
    },
  },
  beforeMount() {
    this.imagesCount = this.images.length;
  },
};
</script>

<style scoped>
.image-height {
  height: 75vh;
}
</style>
