<template>
  <!-- eslint-disable max-len -->
  <div class="sm:mx-16 lg:mx-32">
    <section class="mx-auto">
      <div v-on:click="goBack()" class="sort-button py-0 ml-auto rounded-md text-lg w-20 md:w-16 mr-4 sm:mr-0 mb-4">
        <h1 class="noSelect">←</h1>
      </div>
      <div v-if="user" class="md:flex md:items-start">
        <UserImages v-bind:images="user.images" v-bind:gender="user.gender" class="md:w-7/12 md:order-2 sm:rounded-t md:rounded-r-md md:rounded-l-none"></UserImages>
        <UserProfile class="md:w-5/12 md:order-1 md:overflow-scroll md:border-b md:border-l md:rounded-l-md" v-bind:user="user"></UserProfile>
      </div>
    </section>
  </div>
</template>
<script>
import UserImages from '@/components/app/users/UserImages.vue';
import UserProfile from '@/components/app/users/UserProfile.vue';

export default {
  components: {
    UserImages,
    UserProfile,
  },
  data: () => ({
    user: null,
  }),
  methods: {
    goBack() {
      this.$router.go(-1);
    },
  },
  async beforeMount() {
    const userRequest = await this.$http.get(`/profile/view/${this.$route.params.id}`);
    this.user = userRequest.data.profile;
  },
};
</script>
