<template>
  <!--  eslint-disable max-len -->
  <h1
    v-on:dblclick="likeMessage(message.id, message.is_liked)"
    v-bind:class="{
          'p-2': true,
          'px-4': true,
          'mt-2': true,
          'cursor-pointer': true,
          'inline-block': true,
          'max-w-xs': true,
          'rounded-t-md': true,
          'rounded-br-md': message.to_id === loggedInUserId,
          'rounded-bl-md': message.to_id !== loggedInUserId,
          'bg-purple-matcha': message.to_id === loggedInUserId,
          'bg-green-500': message.to_id !== loggedInUserId,
          'text-white-matcha': true}"
  >{{message.content}}<span class="block text-xs font-light">{{getDateHoursMinutes(message.timestamp)}}</span></h1>
</template>

<script>
export default {
  props: ['message', 'loggedInUserId'],
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
      if (!isLiked) {
        await this.$http.post(`/messages/like/${id}`);
      } else {
        await this.$http.post(`/messages/unlike/${id}`);
      }
    },
  },
};
</script>
