<template>
  <SingleChoice
    v-bind:slide="{
      key: 'location',
      current: slide.current,
      count: slide.count,
      header: 'Location',
      subheader: 'Would you like to share your location to get potential matches closer to you?',
      options: ['yes', 'no'],
      buttonText: slide.buttonText}"
      v-on:saveInput="saveLocation"></SingleChoice>
</template>

<script>
import SingleChoice from '@/components/app/onboarding/SingleChoice.vue';

export default {
  props: ['slide'],
  components: {
    SingleChoice,
  },
  methods: {
    async saveLocation(...args) {
      const [key, value] = args;
      if (key === 'location') {
        if (value === 'yes') {
          navigator.geolocation.getCurrentPosition(
            this.locationAllowed,
            this.locationDenied,
            { enableHighAccuracy: true },
          );
        } else {
          await this.locationDenied();
        }
      }
    },
    async locationAllowed(position) {
      const { latitude } = position.coords;
      const { longitude } = position.coords;
      await this.sendLocation({ lat: latitude, lng: longitude, ip: '0.0.0.0' });
    },
    async locationDenied() {
      let ipRequest = await fetch('https://api.ipify.org?format=json');
      ipRequest = await ipRequest.json();
      const { ip } = ipRequest;
      await this.sendLocation({ ip });
    },
    async sendLocation(data) {
      await this.$http.put('/profile/edit/geolocation', data);
      this.$emit('nextSlide');
    },
  },
};
</script>
