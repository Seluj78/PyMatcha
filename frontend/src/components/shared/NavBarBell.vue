<template>
  <!-- eslint-disable max-len -->
  <div v-if="notificationsFetched" class="ml-auto mr-8 relative pr-1 z-50 outline-none" @focusout="close" tabindex="1">
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
      <div
        v-bind:class="{
        'word-break': true,
        'border-b': true,
        'font-bold': !notification.is_seen,}"
           v-for="(notification, index) in notifications" :key="index + notification.is_seen.toString()">

        <div
          v-if="notification.link_to"
          v-on:click="linkTo(notification.type, notification.link_to)"
          class="py-4 flex items-center word-break cursor-pointer">
          <img v-bind:src="getImage(notification.type)" class="w-4 h-4">
          <h1 class="ml-4">{{notification.content}}</h1>
        </div>
        <div v-else class="py-4 flex items-center word-break">
          <img v-bind:src="getImage(notification.type)" class="w-4 h-4">
          <h1 class="ml-4">{{notification.content}}</h1>
        </div>
      </div>
      <h1 v-if="!notifications.length" class="py-4 flex items-center">No notifications</h1>
    </div>
  </div>
</template>

<script>
import heart from '../../assets/heartOutline.png';
import heartBroken from '../../assets/brokenHeart.png';
import message from '../../assets/message.png';
import view from '../../assets/eye.png';
import match from '../../assets/linkBlack.png';
import superlike from '../../assets/superlikeNotification.png';
import messageLike from '../../assets/likeComment.png';

/* eslint-disable object-curly-newline */
/* eslint-disable consistent-return */
/* eslint-disable max-len */
/* eslint-disable no-await-in-loop */
/* eslint-disable prefer-destructuring */

export default {
  data: () => ({
    notify: false,
    notifications: [],
    notificationsFetched: false,
    showNotifications: false,
    fetchNotificationsIntervalId: null,
  }),
  methods: {
    async linkTo(type, link) {
      await this.toggle();
      if (type === 'match' || type === 'message' || type === 'message_like') {
        if (this.$route.path !== '/matches') {
          await this.$router.push('/matches');
        }
        return;
      }
      if (this.$route.path !== `/${link}`) {
        await this.$router.push(`/${link}`);
      }
    },
    async makeNotificationsSeen() {
      const length = this.notifications.length;
      for (let i = 0; i < length; i += 1) {
        if (!this.notifications[i].is_seen) {
          await this.$http.post(`/notifications/read/${this.notifications[i].id}`);
          this.notifications[i].is_seen = 1;
        }
      }
    },
    async toggle() {
      if (this.showNotifications) {
        this.notify = false;
        await this.makeNotificationsSeen();
      }
      this.showNotifications = !this.showNotifications;
    },
    async close(event) {
      if (!event.currentTarget.contains(event.relatedTarget)) {
        this.showNotifications = false;
        this.notify = false;
        await this.makeNotificationsSeen();
      }
    },
    getImage(type) {
      if (type === 'like') {
        return heart;
      }
      if (type === 'unlike') {
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
      if (type === 'superlike') {
        return superlike;
      }
      if (type === 'message_like') {
        return messageLike;
      }
    },
    async fetchNotifications() {
      const notificationsRequest = await this.$http.get('/notifications');
      this.notifications = notificationsRequest.data.notifications;
      this.notifications = this.notifications.reverse();
    },
    async newNotificationCheck() {
      const notificationsRequest = await this.$http.get('/notifications/unread');
      const { notifications } = notificationsRequest.data;
      this.notify = notifications.length;
    },
    async fetchNewNotifications() {
      const newNotificationsRequest = await this.$http.get('/notifications/unread');
      const newNotifications = newNotificationsRequest.data.notifications;
      if (!newNotifications.length) {
        return;
      }
      await this.fetchNotifications();
      this.notify = true;
    },
  },
  async beforeMount() {
    await this.fetchNotifications();
    await this.newNotificationCheck();
    this.fetchNotificationsIntervalId = setInterval(this.fetchNewNotifications, 10000);
    this.notificationsFetched = true;
  },
  beforeDestroy() {
    window.clearInterval(this.fetchNotificationsIntervalId);
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
