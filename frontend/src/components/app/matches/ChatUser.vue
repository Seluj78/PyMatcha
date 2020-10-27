<template>
  <div v-bind:style="{
      'background-repeat': 'no-repeat',
      'background-position': 'center center',
      'background-size' :'cover',
      'background-image': 'url(' + getImage() + ')'}"
       class="w-10 h-10 rounded-full relative cursor-pointer"
       v-on:click="viewUser()">
    <div
      v-bind:class="{
      'bg-green-500': this.match.is_online,
      'bg-red-500': !this.match.is_online,
      'rounded-full': true,
      'w-3': true,
      'h-3': true}">
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
    async viewUser() {
      await this.$router.push(`/users/${this.match.id}`);
    },
  },
};
</script>
