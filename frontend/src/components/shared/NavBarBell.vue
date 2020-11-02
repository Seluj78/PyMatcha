<template>
  <!-- eslint-disable max-len -->
  <div class="ml-auto mr-8 relative pr-1 z-50 outline-none" @focusout="close" tabindex="1">
    <div class="outline-none">
      <img v-on:click="toggle()" src="../../assets/bell.png" class="w-5 cursor-pointer">
      <div v-on:click="toggle()" v-if="notify" class="w-3 h-3 bg-purple-matcha cursor-pointer rounded-full absolute right-0 bottom-0 ml-2 pl-1"></div>
    </div>
    <div
      id="notifications"
      v-bind:class="{
      'hidden': !showNotifications,
      'px-4': true,
      'overflow-scroll': notifications.length > 3,
      'bg-white': true,
      'shadow': true,
      'w-64': true,
      'h-auto': notifications.length <= 3,
      'h-48': notifications.length > 3,
      'absolute': true,
      'top-0': true,
      'mt-10': true,
      'z-50': true,
      'rounded-md': true}">
      <div v-bind:class="{
        'word-break': true,
        'border-b': true,
        'font-bold': notification.is_seen,}"
           v-for="notification in notifications" :key="notification.id">
        <router-link
          v-bind:to="notification.link_to"
          class="py-4 flex items-center word-break cursor-pointer">
          <img v-bind:src="getImage(notification.type)" class="w-4 h-4">
          <h1 class="ml-4">{{notification.content}}</h1>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import heart from '../../assets/heartOutline.png';
import heartBroken from '../../assets/brokenHeart.png';
import message from '../../assets/message.png';
import view from '../../assets/eye.png';
import match from '../../assets/linkBlack.png';

/* eslint-disable object-curly-newline */
/* eslint-disable consistent-return */

export default {
  data: () => ({
    notify: true,
    notifications: [
      { content: 'Samantha liked you', is_seen: false, type: 'like', id: 1, link_to: 'google.com' },
      { content: 'Bae liked you', id: 2, is_seen: false, type: 'dislike', link_to: 'google.com' },
      { content: 'Samantha liked you', id: 3, is_seen: false, type: 'message', link_to: 'google.com' },
      { content: 'Bae liked you', id: 4, is_seen: false, type: 'match', link_to: 'google.com' },
      { content: 'Samantha liked you', id: 5, is_seen: true, type: 'view', link_to: 'google.com' },
      { content: 'Bae liked you', id: 6, is_seen: true, type: 'like', link_to: 'google.com' },
      { content: 'Samantha liked you', id: 7, is_seen: true, type: 'like', link_to: 'google.com' },
      { content: 'Bae liked you', id: 8, is_seen: true, type: 'like', link_to: 'google.com' },
      { content: 'Samantha liked you', id: 9, is_seen: true, type: 'like', link_to: 'google.com' },
      { content: 'Bae liked youBae liked youBae liked youBae liked youBae liked youBae liked you', id: 10, is_seen: true, type: 'like', link_to: 'google.com' },
    ],
    showNotifications: false,
  }),
  methods: {
    toggle() {
      this.showNotifications = !this.showNotifications;
    },
    close(event) {
      if (!event.currentTarget.contains(event.relatedTarget)) {
        this.showNotifications = false;
        this.notify = false;
      }
    },
    getImage(type) {
      if (type === 'like') {
        return heart;
      }
      if (type === 'dislike') {
        return heartBroken;
      }
      if (type === 'match') {
        return match;
      }
      if (type === 'view') {
        return view;
      }
      if (type === 'message') {
        return message;
      }
    },
  },
};
</script>

<style>

#notifications {
  @apply -ml-64;
}

@screen md {
  #notifications {
    @apply ml-0;
  }
}
</style>
