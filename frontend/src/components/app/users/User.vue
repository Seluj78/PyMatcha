<template>
  <!-- eslint-disable max-len -->
  <div class="sm:mx-16 lg:mx-32">
    <div v-if="error" class="mx-auto flex items-center justify-center mt-32">
      {{error}}
    </div>
    <div v-if="!user && !error" class="mx-auto flex items-center justify-center mt-32">
      <img class="h-36" src="../../../assets/loading.svg">
    </div>
    <section v-if="user && !error && imagesSorted" class="mx-auto">
      <div v-on:click="goBack()" class="sort-button py-0 ml-auto rounded-md text-lg w-20 md:w-16 mr-4 sm:mr-0 mb-4">
        <h1 class="noSelect">←</h1>
      </div>
      <div class="md:flex md:items-start">
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
    error: null,
    imagesSorted: false,
  }),
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    sortImages() {
      const userImagesLength = this.user.images.length;
      for (let i = 0; i < userImagesLength; i += 1) {
        if (this.user.images[i].is_primary && i !== 0) {
          this.user.images.splice(0, 0, this.user.images[i]);
          this.user.images.splice(i + 1, 1);
          return;
        }
      }
    },
  },
  watch: {
    async $route() {
      this.user = null;
      this.imagesSorted = false;
      const userRequest = await this.$http.get(`/profile/view/${this.$route.params.id}`, { accessTokenRequired: true });
      this.user = userRequest.data.profile;
      this.sortImages();
      this.imagesSorted = true;
    },
  },
  async beforeMount() {
    try {
      const userRequest = await this.$http.get(`/profile/view/${this.$route.params.id}`, { accessTokenRequired: true });
      this.user = userRequest.data.profile;
      this.sortImages();
      this.imagesSorted = true;
    } catch (error) {
      this.error = error.response.data.error.message;
    }
  },
};
</script>
