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
      'p-4': true,
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
      <div v-for="notification in notifications" :key="notification.id">{{notification.text}}</div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    notify: true,
    notifications: [
      { text: 'Samantha liked you', id: 1 },
      { text: 'Bae liked you', id: 2 },
      { text: 'Samantha liked you', id: 3 },
      { text: 'Bae liked you', id: 4 },
      { text: 'Samantha liked you', id: 5 },
      { text: 'Bae liked you', id: 6 },
      { text: 'Samantha liked you', id: 7 },
      { text: 'Bae liked you', id: 8 },
      { text: 'Samantha liked you', id: 9 },
      { text: 'Bae liked you', id: 10 },
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
