<template>
  <!-- eslint-disable max-len -->
  <div class="sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Browse'"></NavBar>
    <section class="mx-auto">
      <div v-on:click="goBack()" class="sort-button py-0 ml-auto rounded-md text-lg w-20 md:w-16 mr-4 sm:mr-0 mb-4">
        <h1 class="noSelect">←</h1>
      </div>
      <div v-if="user" class="md:flex md:items-start">
        <UserImages v-bind:images="user.images" class="md:w-2/3 md:order-2 sm:rounded md:rounded-r-md md:rounded-l-none"></UserImages>
        <UserProfile class="md:w-1/3 md:order-1 md:overflow-scroll md:border md:rounded-l-md" v-bind:user="user"></UserProfile>
      </div>
    </section>
  </div>
</template>
<script>
import UserImages from '@/components/app/users/UserImages.vue';
import UserProfile from '@/components/app/users/UserProfile.vue';
import NavBar from '@/components/shared/NavBar.vue';

export default {
  components: {
    UserImages,
    UserProfile,
    NavBar,
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
