<template>
  <!--  eslint-disable max-len -->
  <div class="noSelect mt-2 relative">
    <img v-if="message.to_id !== loggedInUserId && message.is_liked"
      src="../../../assets/heart.png" class="w-6 mr-2 inline-block"
      v-on:dblclick="likeMessage(message.id, message.is_liked)">
    <h1
      v-on:dblclick="likeMessage(message.id, message.is_liked)"
      v-bind:class="{
            'p-2': true,
            'px-4': true,
            'cursor-pointer': message.to_id === loggedInUserId,
            'inline-block': true,
            'max-w-xs': true,
            'rounded-t-md': true,
            'rounded-br-md': message.to_id === loggedInUserId,
            'rounded-bl-md': message.to_id !== loggedInUserId,
            'bg-purple-matcha': message.to_id === loggedInUserId,
            'bg-green-500': message.to_id !== loggedInUserId,
            'text-white-matcha': true}"
    >{{message.content}}<span class="block text-xs font-light">{{getDateHoursMinutes(message.timestamp)}}</span></h1>
    <img v-if="message.to_id === loggedInUserId && message.is_liked"
         src="../../../assets/heart.png" class="w-6 ml-2 inline-block absolute heart"
         v-on:dblclick="likeMessage(message.id, message.is_liked)">
  </div>
</template>

<script>
export default {
  props: ['messagePassed', 'loggedInUserId'],
  data: () => ({
    message: {},
  }),
  methods: {
    getDateHoursMinutes(timestamp) {
      if (!timestamp) {
        return '';
      }
      const splitBySpace = timestamp.split(' ');
      const splitByColon = splitBySpace[4].split(':');
      return `${splitByColon[0]}:${splitByColon[1]}`;
    },
    async likeMessage(id, isLiked) {
      if (this.message.to_id !== this.loggedInUserId) {
        return;
      }
      if (!isLiked) {
        this.message.is_liked = true;
        await this.$http.post(`/messages/like/${id}`);
      } else {
        this.message.is_liked = false;
        await this.$http.post(`/messages/unlike/${id}`);
      }
    },
  },
  beforeMount() {
    this.message = this.messagePassed;
  },
};
</script>

<style>
.heart {
  top: 50%;
  transform: translateY(-50%);
}
</style>
