<template>
  <!-- eslint-disable max-len -->
  <div class="w-full md:w-auto md:mx-16 lg:mx-32 relative md:flex items-start h-auto md:mb-16">
    <div v-if="!settingsFetched" class="mx-auto flex items-center justify-center mt-32">
      <img class="h-36" src="../../assets/loading.svg">
    </div>
    <section v-if="settingsFetched" class="w-auto md:max-w-xss md:shadow-md md:rounded-md">
      <div class="w-full md:hidden h-1 bg-white-matcha"></div>
      <div class="md:border-b profile-card text-wrap p-16 md:py-8 flex flex-col w-full md:rounded-t-md">
        <div class="mx-auto overflow-hidden w-48 h-48 md:w-24 md:h-24 rounded-full">
          <img class="w-full" v-bind:src="getImage()">
        </div>
        <h1 class="w-full text-center text-3xl md:text-base mt-4 text-white-matcha md:text-gray-matcha capitalize">
          {{this.$store.getters.getLoggedInUser.first_name}} {{this.$store.getters.getLoggedInUser.last_name}}</h1>
        <div class="text-white-matcha md:text-gray-matcha w-full flex justify-center text-center mt-4 max-w-xs mx-auto">
          <div class="mr-4">
            <h1 class="font-bold">{{userViewsReceived}}</h1>
            <h1 class="text-xs">Views</h1>
          </div>
          <div class="ml-4">
            <h1 class="font-bold">{{this.$store.getters.getLoggedInUser.likes.received.length}}</h1>
            <h1 class="text-xs">Likes</h1>
          </div>
        </div>
      </div>
      <div class="px-8 py-2 md:py-4 md:px-0 w-full">
        <MenuButton v-on:click.native="showSetting('account')" v-bind:class="{'md:px-8':true, 'md:bg-purple-200': getShow === 'account'}" v-bind:text="'Account'"></MenuButton>
        <hr class="bg-gray-300 w-full md:hidden">
        <MenuButton v-on:click.native="showSetting('profile')" v-bind:class="{'md:px-8':true, 'md:bg-purple-200': getShow === 'profile'}" v-bind:text="'Profile'"></MenuButton>
      </div>
    </section>
    <section v-if="getShow === 'account' && settingsFetched" class="flex flex-col items-center z-10 absolute bg-white-matcha px-8 md:pb-8 w-full top-0 left-0 h-full md:h-auto md:ml-4 md:relative md:shadow-md md:rounded-md">
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
    <section v-if="getShow === 'profile' && settingsFetched" class="flex flex-col items-start z-10 absolute bg-white-matcha w-full top-0 left-0 md:ml-4 md:relative md:shadow-md md:rounded-md">
      <div class="px-8 w-full">
        <SectionHeader class="mx-auto" v-bind:name="'profile'" v-on:click.native="closeSetting()"></SectionHeader>
      </div>
      <div class="pb-8 pt-4 px-8 w-full">
        <div class="mx-auto max-w-sm">
          <h1 class="inline-block mr-4 text-gray-matcha">I am</h1>
          <DropdownDisplayChoice
            class="inline-block"
            v-on:save-single-choice="saveSingleChoice"
            v-bind:name="'gender'"
            v-bind:starting-option="this.$store.getters.getLoggedInUser.gender"
            v-bind:options="['male', 'female', 'other']"></DropdownDisplayChoice>
        </div>
        <div class="mt-4 mx-auto max-w-sm">
          <h1 class="inline-block mr-4 text-gray-matcha">Sexuality</h1>
          <DropdownDisplayChoice
            class="inline-block"
            v-on:save-single-choice="saveSingleChoice"
            v-bind:name="'sexuality'"
            v-bind:starting-option="this.$store.getters.getLoggedInUser.orientation"
            v-bind:options="['heterosexual', 'homosexual', 'bisexual', 'other']"></DropdownDisplayChoice>
        </div>
        <div class="mt-4 mx-auto max-w-sm">
          <h1 class="inline-block mr-3 text-gray-matcha">Interests</h1>
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
            v-on:save-multiple-choice="saveMultipleChoice"></DropdownDisplayChoices>
        </div>
      </div>
      <div class="py-4 px-8 border-t border-gray-300 w-full">
        <AccountInput
          class="mx-auto"
          v-bind:name="'Bio'"
          v-bind:type="'bio'"
          v-bind:currentValuePassed="this.$store.getters.getLoggedInUser.bio"></AccountInput>
      </div>
      <div class="text-center px-8 py-8 border-t border-gray-300 w-full">
        <h1 class="inline-block mr-3 font-bold text-gray-matcha leading-none">Location</h1>
        <h1 class="text-md font-normal opacity-50 text-gray-matcha mx-auto pb-2 max-w-sm">If you refused sharing location, it will be approximated from your computer address </h1>
        <h1 v-if="!locationUpdateSuccess" class="mx-auto onboarding-sub-container-content-button-outline max-w-sm border font-normal mt-2 px-2 cursor-pointer" v-on:click="updateLocation()">Update current location</h1>
        <h1 v-else class="mx-auto onboarding-sub-container-content-button-outline max-w-sm border font-normal mt-2 px-2 cursor-pointer text-green-500">Success</h1>
      </div>
      <div class="text-center py-8 w-full px-8 border-t border-gray-300">
        <h1 class="font-bold text-gray-matcha">Images<span class="text-md font-normal ml-2 opacity-50 text-gray-matcha">{{this.$store.getters.getLoggedInUser.images.length}} / 5</span></h1>
        <div class="auth-sub-container-error mt-8" v-if="image.error">
          <h1 class="auth-sub-container-error-message">{{image.error}}</h1>
        </div>
        <button v-if="this.$store.getters.getLoggedInUser.images.length < 6" class="overflow-hidden relative onboarding-sub-container-content-button-outline border w-full max-w-sm my-4">
          <input style="padding-left: 100%;" class="cursor-pointer opacity-0 absolute top-0 left-0 w-full h-full rounded-md" type="file" v-on:change="selectFile()" ref="file">
          <img src="../../assets/onboarding/cloudPurple.png" class="w-8 mx-auto">
        </button>
        <ProfileImage
          v-for="image in this.$store.getters.getLoggedInUser.images"
          :key="image.id"
          v-bind:image="image"
          v-on:make-primary-image="makePrimaryImage"
          v-on:delete-image="deleteImage"></ProfileImage>
      </div>
    </section>
  </div>
</template>

<script>
/* eslint-disable prefer-destructuring */
/* eslint-disable prefer-const */
import MenuButton from '@/components/app/settings/MenuButton.vue';
import SectionHeader from '@/components/app/settings/SectionHeader.vue';
import AccountInput from '@/components/app/settings/AccountInput.vue';
import DropdownDisplayChoice from '@/components/shared/DropdownDisplayChoice.vue';
import DropdownDisplayChoices from '@/components/shared/DropdownDisplayChoices.vue';
import ProfileImage from '@/components/app/settings/ProfileImage.vue';
import imageMan from '../../assets/recommendations/avatars/man1.png';
import imageWoman from '../../assets/recommendations/avatars/woman1.png';
import imageOther from '../../assets/recommendations/avatars/other.png';

export default {
  components: {
    MenuButton,
    AccountInput,
    SectionHeader,
    DropdownDisplayChoice,
    DropdownDisplayChoices,
    ProfileImage,
  },
  data: () => ({
    userInterests: [],
    userViewsReceived: 0,
    show: '',
    image: {
      error: null,
    },
    locationUpdateSuccess: false,
    settingsFetched: false,
  }),
  computed: {
    getShow() {
      return this.show;
    },
  },
  methods: {
    async updateLocation() {
      navigator.geolocation.getCurrentPosition(
        this.locationAllowed,
        this.locationDenied,
        { enableHighAccuracy: true },
      );
    },
    async locationAllowed(position) {
      const { latitude } = position.coords;
      const { longitude } = position.coords;
      const locationData = { lat: latitude, lng: longitude, ip: '0.0.0.0' };
      await this.$http.put('/profile/edit/geolocation', locationData);
      this.locationUpdateSuccess = true;
      setTimeout(() => {
        this.locationUpdateSuccess = false;
      }, 3000);
    },
    async locationDenied() {
      let ipRequest = await fetch('https://api.ipify.org?format=json');
      ipRequest = await ipRequest.json();
      const { ip } = ipRequest;
      const locationData = { ip };
      await this.$http.put('/profile/edit/geolocation', locationData);
      this.locationUpdateSuccess = true;
      setTimeout(() => {
        this.locationUpdateSuccess = false;
      }, 3000);
    },
    async selectFile() {
      this.image.error = '';
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const file = this.$refs.file.files[0];

      if (!allowedTypes.includes(file.type)) {
        this.image.error = 'Only images allowed';
        return;
      }
      if (file.size > 2000000) {
        this.image.error = 'File too large';
        return;
      }
      const formData = new FormData();
      formData.append('file[]', file);
      if (this.$store.getters.getLoggedInUser.images.length) {
        await this.$http.post('/profile/images?is_primary=false', formData);
      } else {
        await this.$http.post('/profile/images?is_primary=true', formData);
      }
      const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`);
      await this.$store.dispatch('login', user.data);
    },
    async deleteImage(...args) {
      const [imageId] = args;
      await this.$http.delete(`/profile/images/${imageId}`);
      const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`);
      await this.$store.dispatch('login', user.data);
    },
    async makePrimaryImage(...args) {
      const [imageId] = args;
      await this.$http.put(`/profile/images/${imageId}`);
      const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`);
      await this.$store.dispatch('login', user.data);
    },
    async saveSingleChoice(...args) {
      const [key, value] = args;
      if (key === 'gender') {
        await this.$http.patch('/profile/edit/gender', { gender: value });
      } else if (key === 'sexuality') {
        await this.$http.patch('/profile/edit/orientation', { orientation: value });
      }
      const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`);
      await this.$store.dispatch('login', user.data);
    },
    async saveMultipleChoice(...args) {
      const [key, value] = args;
      if (key === 'interests') {
        await this.$http.patch('/profile/edit/tags', { tags: value });
      }
      const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`);
      await this.$store.dispatch('login', user.data);
    },
    showSetting(setting) {
      this.show = setting;
      window.scrollTo(0, 0);
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
      for (let i = 0; i < this.$store.getters.getLoggedInUser.images.length; i += 1) {
        if (this.$store.getters.getLoggedInUser.images[i].is_primary) {
          return this.$store.getters.getLoggedInUser.images[i].link;
        }
      }
      return this.$store.getters.getLoggedInUser.images[0].link;
    },
    openSectionOnMd(e) {
      if (e.target.innerWidth >= 768 && this.show === '') {
        this.show = 'profile';
      }
    },
  },
  async beforeMount() {
    window.addEventListener('resize', this.openSectionOnMd);
    if (window.innerWidth >= 768) {
      this.show = 'profile';
    }
    const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`);
    await this.$store.dispatch('login', user.data);
    const tags = this.$store.getters.getLoggedInUser.tags;
    for (let i = 0; i < tags.length; i += 1) {
      this.userInterests.push(tags[i].name);
    }
    const userViewsReceivedRequest = await this.$http.get('/history/viewed/me');
    this.userViewsReceived = userViewsReceivedRequest.data.viewed_me.length;
    this.settingsFetched = true;
  },
};
</script>

<style scoped>
.recommendation-card {
  /*width: 24rem;*/
  height: 20rem;
  /*box-shadow: inset 0 -8rem 1rem rgba(0, 0, 0, 0.3);*/
}

@screen md {
  .recommendation-card {
    height: 10rem;
  }
}

.profile-card {
  background-image: linear-gradient(315deg, #6e72fc 0%, #6e72fc 74%);
}

@screen md {
  .profile-card {
    background-image: linear-gradient(315deg, #FFFFFE 0%, #FFFFFE 74%);
  }
}
</style>
