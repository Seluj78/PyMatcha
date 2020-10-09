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
        <SectionHeader v-bind:name="'account'" v-on:click.native="closeSetting()"></SectionHeader>
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
      <section v-if="getShow === 'profile'" class="profile-section flex flex-col items-start z-10 absolute bg-white-matcha px-8 pb-4 w-full top-0 left-0 h-screen md:ml-4 md:relative md:shadow-md md:rounded-md">
        <SectionHeader v-bind:name="'profile'" v-on:click.native="closeSetting()"></SectionHeader>
        <div>
          <h1 class="inline-block mr-4">I am</h1>
          <DropdownDisplayChoice
            class="inline-block"
            v-on:saveSingleChoice="saveSingleChoice"
            v-bind:name="'gender'"
            v-bind:starting-option="this.$store.getters.getLoggedInUser.gender"
            v-bind:options="['male', 'female', 'other']"></DropdownDisplayChoice>
        </div>
        <div class="mt-4">
          <h1 class="inline-block mr-4">Sexuality</h1>
          <DropdownDisplayChoice
            class="inline-block"
            v-on:saveSingleChoice="saveSingleChoice"
            v-bind:name="'gender'"
            v-bind:starting-option="this.$store.getters.getLoggedInUser.orientation"
            v-bind:options="['heterosexual', 'homosexual', 'bisexual', 'other']"></DropdownDisplayChoice>
        </div>
        <div class="mt-4">
          <h1 class="inline-block mr-3">Interests</h1>
          <DropdownDisplayChoices
            class="inline-block"
            v-bind:options="[
          'swimming', 'wine', 'reading', 'foodie', 'netflix', 'music', 'yoga', 'golf',
          'photography', 'baking', 'shopping', 'outdoors', 'art', 'travel', 'hiking',
          'running', 'volunteering', 'cycling', 'climbing', 'tea', 'fishing', 'soccer',
          'museum', 'dancing', 'surfing', 'karaoke', 'parties', 'diy',
          'walking', 'cat lover', 'movies', 'gardening', 'trivia', 'working out',
          'cooking', 'gamer', 'brunch', 'blogging', 'picknicking', 'athlete',
          'dog lover', 'politics', 'environmentalism', 'instagram', 'spirituality',
          'language exchange', 'sports', 'comedy', 'fashion', 'disney', 'vlogging',
          'astrology', 'board games', 'craft beer', 'coffee', 'writer',
          ]"
            v-bind:startingOptions="userInterests"
            v-bind:min="3"
            v-bind:max="10"
            v-bind:name="'interests'"
            v-on:saveMultipleChoice="saveMultipleChoice"></DropdownDisplayChoices>
        </div>
        <div class="mt-4">
          <AccountInput
            v-bind:name="'Bio'"
            v-bind:type="'bio'"
            v-bind:currentValuePassed="this.$store.getters.getLoggedInUser.bio"></AccountInput>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
/* eslint-disable prefer-destructuring */
import NavBar from '@/components/shared/NavBar.vue';
import MenuButton from '@/components/app/settings/MenuButton.vue';
import SectionHeader from '@/components/app/settings/SectionHeader.vue';
import AccountInput from '@/components/app/settings/AccountInput.vue';
import DropdownDisplayChoice from '@/components/shared/DropdownDisplayChoice.vue';
import DropdownDisplayChoices from '@/components/shared/DropdownDisplayChoices.vue';
import imageMan from '../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../assets/recommendations/avatars/other.png';

export default {
  components: {
    NavBar,
    MenuButton,
    AccountInput,
    SectionHeader,
    DropdownDisplayChoice,
    DropdownDisplayChoices,
  },
  data: () => ({
    userInterests: [],
    show: '',
  }),
  computed: {
    getShow() {
      return this.show;
    },
  },
  methods: {
    saveSingleChoice(...args) {
      const [key, value] = args;
      if (key === 'gender') {
        console.log(value);
      }
    },
    saveMultipleChoice(...args) {
      const [key, value] = args;
      if (key === 'interests') {
        console.log(value);
      }
    },
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
    const tags = this.$store.getters.getLoggedInUser.tags;
    for (let i = 0; i < tags.length; i += 1) {
      this.userInterests.push(tags[i].name);
    }
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
