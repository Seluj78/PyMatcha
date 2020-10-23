<template>
  <div v-bind:style="{
      'background-repeat': 'no-repeat',
      'background-position': 'center center',
      'background-size' :'cover',
      'background-image': 'url(' + getImage() + ')'}"
      class="w-12 h-12 sm:w-16 sm:h-16 rounded-full relative cursor-pointer"
      v-on:click="chat()">
    <div
      v-bind:class="{
      'bg-green-500': this.match.is_online,
      'bg-red-500': !this.match.is_online,
      'rounded-full': true,
      'w-4': true,
      'h-4': true}">
    </div>
  </div>
</template>

<script>
/* eslint-disable no-else-return */
import imageMan from '../../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../../assets/recommendations/avatars/other.png';

export default {
  props: ['match'],
  methods: {
    getImage() {
      const { images } = this.match;
      if (images.length) {
        for (let i = 0; i < images.length; i += 1) {
          if (images[i].is_primary) {
            return images[i].link;
          }
        }
        return images[0].link;
      } else if (this.match.gender === 'male') {
        return imageMan;
      } else if (this.match.gender === 'female') {
        return imageWoman;
      }
      return imageOther;
    },
    async chat() {
      await this.$router.push(`/chat/${this.match.id}`);
    },
  },
};
</script>
