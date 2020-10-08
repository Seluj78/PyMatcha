<template>
  <!-- eslint-disable max-len -->
  <div>
    <NavBar class="px-4 sm:px-16 lg:px-32" v-bind:currentRoute="'Settings'"></NavBar>
    <div class="w-full md:w-auto md:mx-16 lg:mx-32 relative md:flex items-start h-auto md:mb-16 lg:mb-32">
      <section class="w-full md:max-w-xs md:shadow-md md:rounded-md">
        <div class="w-full md:hidden h-1 bg-white-matcha"></div>
        <div class="text-wrap bg-white-matcha recommendation-card w-full sm:rounded-md"
             v-bind:style="{
            'background-repeat': 'no-repeat',
            'background-position': 'center center',
            'background-size' :'cover',
            'background-image': 'url(' + getImage() + ')'}">
<!--          <h1 class="absolute bottom-0 w-full text-center pb-8 text-4xl text-white-matcha capitalize">-->
<!--            {{this.$store.getters.getLoggedInUser.first_name}} {{this.$store.getters.getLoggedInUser.last_name}}</h1>-->
        </div>
        <div class="px-8 pb-2 md:pt-2 md:pt-4 md:py-0 md:px-0 w-full">
          <h1 class="text-4xl md:text-2xl md:font-bold text-gray-matcha text-center md:text-left md:px-8 font-bold md:font-normal mt-4 md:mb-1 md:mt-0">Settings</h1>
          <MenuButton v-on:click.native="showSetting('account')" v-bind:class="{'md:px-8':true, 'md:bg-gray-200': getShow === 'account'}" v-bind:text="'Account'"></MenuButton>
          <hr class="bg-gray-300 w-full md:hidden">
          <MenuButton v-on:click.native="showSetting('profile')" v-bind:class="{'md:px-8':true, 'md:bg-gray-200': getShow === 'profile'}" v-bind:text="'Profile'"></MenuButton>
        </div>
      </section>
      <section v-if="getShow === 'account'" class="flex flex-col items-start z-10 absolute bg-white-matcha px-8 pb-4 w-full top-0 left-0 h-screen md:h-auto md:ml-4 md:relative md:shadow-md md:rounded-md">
        <div class="flex justify-between items-center w-full my-4 lg:mb-0">
          <h1 class="text-3xl md:hidden text-gray-matcha">Account</h1>
          <div class="md:hidden sort-button rounded-md text-lg w-12" v-on:click="closeSetting()">
            <h1 class="noSelect">←</h1>
          </div>
        </div>
        <AccountInput
          v-bind:name="'First Name'"
          v-bind:type="'firstName'"
          v-bind:currentValuePassed="this.$store.getters.getLoggedInUser.first_name"></AccountInput>
        <AccountInput
          v-bind:name="'Last Name'"
          v-bind:type="'lastName'"
          v-bind:currentValuePassed="this.$store.getters.getLoggedInUser.last_name"></AccountInput>
        <AccountInput
          v-bind:name="'Email'"
          v-bind:type="'email'"
          v-bind:currentValuePassed="this.$store.getters.getLoggedInUser.email"></AccountInput>
        <AccountInput
          v-bind:name="'Username'"
          v-bind:type="'username'"
          v-bind:currentValuePassed="this.$store.getters.getLoggedInUser.username"></AccountInput>
        <AccountInput
          v-bind:name="'Password'"
          v-bind:type="'password'"
          v-bind:currentValuePassed="''"></AccountInput>
      </section>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/shared/NavBar.vue';
import MenuButton from '@/components/app/settings/MenuButton.vue';
import AccountInput from '@/components/app/settings/AccountInput.vue';
import imageMan from '../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../assets/recommendations/avatars/other.png';

export default {
  components: {
    NavBar,
    MenuButton,
    AccountInput,
  },
  data: () => ({
    userInfo: {},
    show: '',
  }),
  computed: {
    getShow() {
      return this.show;
    },
  },
  methods: {
    showSetting(setting) {
      this.show = setting;
    },
    closeSetting() {
      this.show = '';
    },
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
  height: 20rem;
  /*box-shadow: inset 0 -8rem 1rem rgba(0, 0, 0, 0.3);*/
}
</style>
