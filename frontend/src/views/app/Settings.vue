<template>
  <!-- eslint-disable max-len -->
  <div>
    <NavBar class="px-4 sm:px-16 lg:px-32" v-bind:currentRoute="'Settings'"></NavBar>
    <div class="w-full md:mx-16 lg:mx-32">
      <section class="w-full md:max-w-xs md:shadow-md md:rounded-md">
        <div class="relative text-wrap shadow-inner recommendation-card w-full sm:rounded-md"
             v-bind:style="{
            'background-repeat': 'no-repeat',
            'background-position': 'center center',
            'background-size' :'cover',
            'background-image': 'url(' + getImage() + ')'}">
<!--          <h1 class="absolute bottom-0 w-full text-center pb-8 text-4xl text-white-matcha capitalize">-->
<!--            {{this.$store.getters.getLoggedInUser.first_name}} {{this.$store.getters.getLoggedInUser.last_name}}</h1>-->
        </div>
        <div class="px-8 py-2 md:pt-4 md:py-0 md:px-0 w-full">
          <h1 class="text-4xl text-gray-matcha text-center md:text-left md:px-8 font-bold md:font-normal my-4 md:mb-1 md:mt-0">Settings</h1>
          <MenuButton v-bind:class="{'md:px-8':true, 'md:bg-gray-200': show === 'account'}" v-bind:text="'Account'"></MenuButton>
          <hr class="bg-gray-300 w-full md:hidden">
          <MenuButton v-bind:class="{'md:px-8':true, 'md:bg-gray-200': show === 'profile'}" v-bind:text="'Profile'"></MenuButton>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/shared/NavBar.vue';
import MenuButton from '@/components/app/settings/MenuButton.vue';
import imageMan from '../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../assets/recommendations/avatars/other.png';

export default {
  components: {
    NavBar,
    MenuButton,
  },
  data: () => ({
    userInfo: {},
    show: 'account',
  }),
  methods: {
    getImage() {
      if (this.$store.getters.getLoggedInUser.images.length === 0) {
        if (this.$store.getters.getLoggedInUser.gender === 'male') {
          return imageMan;
        }
        if (this.$store.getters.getLoggedInUser.gender === 'female') {
          return imageWoman;
        }
        return imageOther;
      }
      return this.$store.getters.getLoggedInUser.images[0].link;
    },
  },
  beforeMount() {
    console.log(this.$store.getters.getLoggedInUser);
    // const userInfoRequest = this.$http.get();
  },
};
</script>

<style scoped>
.recommendation-card {
  /*width: 24rem;*/
  height: 24rem;
  /*box-shadow: inset 0 -8rem 1rem rgba(0, 0, 0, 0.3);*/
}
</style>
