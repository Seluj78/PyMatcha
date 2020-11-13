<template>
  <!-- eslint-disable max-len -->
  <div
      v-if="index < showCount"
      v-on:click="viewUser(recommendation.id)"
      class="flex flex-col justify-end shadow-inner recommendation-card rounded-md cursor-pointer"
       v-bind:style="{
      'background-repeat': 'no-repeat',
      'background-position': 'center center',
      'background-size' :'cover',
      'background-image': 'url(' + getPrimaryImage() + ')'}">
    <div class="p-8 text-white">
      <div class="flex items-center">
        <img v-if="this.recommendation.is_online" class="w-3 h-3" src="../../../assets/recommendations/online.png">
        <img v-else class="w-3 h-3" src="../../../assets/recommendations/offline.png">
        <h1 v-if="this.recommendation.is_online" class="text-lg ml-2 leading-none">online</h1>
        <h1 v-else class="text-lg ml-2 leading-none">offline</h1>
      </div>
      <div class="flex items-end my-2">
        <h1 class="text-4xl font-bold leading-none">{{this.recommendation.first_name}}</h1>
        <h1 class="text-2xl ml-2 leading-none mb-1">{{this.recommendation.age}}</h1>
      </div>
      <h1 class="text-lg">{{this.recommendation.distance}}km away</h1>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-else-return */
/* eslint-disable max-len */

import imageMan from '../../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../../assets/recommendations/avatars/other.png';

export default {
  props: ['recommendation', 'index', 'showCount'],
  methods: {
    async viewUser(id) {
      await this.$router.push(`/users/${id}`);
    },
    getPrimaryImage() {
      const userImages = this.recommendation.images;
      let imageForShowcase;
      for (let i = 0; i < userImages.length; i += 1) {
        if (userImages[i].is_primary) {
          imageForShowcase = userImages[i].link;
        } else if (!userImages[i].is_primary && !imageForShowcase) {
          imageForShowcase = userImages[i].link;
        }
      }
      if (imageForShowcase) {
        return imageForShowcase;
      }
      if (this.recommendation.gender === 'male') {
        return imageMan;
      } else if (this.recommendation.gender === 'female') {
        return imageWoman;
      }
      return imageOther;
    },
  },
};
</script>

<style scoped>
.recommendation-card {
  /*width: 24rem;*/
  height: 24rem;
  box-shadow: inset 0 -8rem 1rem rgba(0, 0, 0, 0.3);
}

@screen lg {
  .recommendation-card {
    height:32rem;
  }
}
</style>
