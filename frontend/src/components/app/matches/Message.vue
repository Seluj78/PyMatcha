<template>
  <!--  eslint-disable max-len -->
  <div class="flex border-b py-4 cursor-pointer" v-on:click="chat()">
    <div>
      <div v-bind:style="{
          'background-repeat': 'no-repeat',
          'background-position': 'center center',
          'background-size' :'cover',
          'background-image': 'url(' + getImage() + ')'}"
           class="w-12 h-12 rounded-full relative">
        <div
          v-bind:class="{
          'bg-green-500': this.match.is_online,
          'bg-red-500': !this.match.is_online,
          'rounded-full': true,
          'w-3': true,
          'h-3': true}">
        </div>
      </div>
    </div>
    <div class="ml-4 w-full">
      <div class="flex justify-between">
        <h1 class="font-bold">{{this.match.first_name}}</h1>
        <h1 class="text-sm opacity-50">{{this.message.last_message_timestamp_ago}}</h1>
      </div>
      <h1 v-bind:class="{'opacity-50': this.message.is_unseen}">{{getMessage}}</h1>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-else-return */
import imageMan from '@/assets/recommendations/avatars/man1.png';
import imageWoman from '@/assets/recommendations/avatars/woman1.png';
import imageOther from '@/assets/recommendations/avatars/other.png';

export default {
  props: ['message'],
  data: () => ({
    match: null,
  }),
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
      this.$emit('chat', this.match.id);
    },
  },
  computed: {
    getMessage() {
      if (this.message.last_message_content.length > 20) {
        return `${this.message.last_message_content.substring(1, 20)}...`;
      }
      return this.message.last_message_content;
    },
  },
  beforeMount() {
    this.match = this.message.with_user;
  },
};
</script>
