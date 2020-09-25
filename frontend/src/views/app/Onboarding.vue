<template>
  <!-- eslint-disable max-len -->
  <div class="onboarding-container">
    <Introduction
      v-bind:slide="{buttonText}"
      v-on:nextSlide="nextSlide"
      v-if="slideCurrent === 0"></Introduction>
    <SingleChoice
      v-bind:slide="{
      key: 'birthdate',
      current: slideCurrent,
      count: slideCount,
      header: 'My age',
      options: generateAllowedAge(),
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 1"></SingleChoice>
    <SingleChoice
      v-bind:slide="{
      key: 'gender',
      current: slideCurrent,
      count: slideCount,
      header: 'I am',
      options: ['male', 'female', 'other'],
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 2"></SingleChoice>
    <SingleChoice
      v-bind:slide="{
      key: 'orientation',
      current: slideCurrent,
      count: slideCount,
      header: 'Sexuality',
      options: ['heterosexual', 'homosexual', 'bisexual', 'other'],
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 3"></SingleChoice>
    <MultipleChoice
      v-bind:slide="{
      key: 'tags' ,
      current: slideCurrent,
      count: slideCount,
      header: 'Interests',
      options: [
        'swimming', 'wine', 'reading', 'foodie', 'netflix', 'music', 'yoga', 'golf',
        'photography', 'baking', 'shopping', 'outdoors', 'art', 'travel', 'hiking',
        'running', 'volunteering', 'cycling', 'climbing', 'tea', 'fishing', 'soccer',
        'museum', 'dancing', 'surfing', 'karaoke', 'parties', 'diy',
        'walking', 'cat lover', 'movies', 'gardening', 'trivia', 'working out',
        'cooking', 'gamer', 'brunch', 'blogging', 'picknicking', 'athlete',
        'dog lover', 'politics', 'environmentalism', 'instagram', 'spirituality',
        'language exchange', 'sports', 'comedy', 'fashion', 'disney', 'vlogging',
        'astrology', 'board games', 'craft beer', 'coffee', 'writer',
      ],
      minOptionsForSelection: 3,
      maxOptionsForSelection: 10,
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 4"></MultipleChoice>
    <MainAndSecondaryImagesUpload
      v-bind:slide="{
      key: 'images',
      current: slideCurrent,
      count: slideCount,
      header: 'Images',
      mainImageExplanation: 'Profile image',
      secondaryImageExplanation: 'Extra image',
      maxImagesAllowed: 5,
      buttonText}"
      v-on:nextSlide="nextSlide"
      v-if="slideCurrent === 5"></MainAndSecondaryImagesUpload>
    <Textblock
      v-bind:slide="{
      key: 'bio',
      current: slideCurrent,
      count: slideCount,
      minTextareaLength: 51,
      maxTextareaLength: 200,
      placeholder: 'I am best described as ...',
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 6"></Textblock>
    <Location
      v-bind:slide="{
      key: 'location',
      current: slideCurrent,
      count: slideCount,
      buttonText}"
      v-on:nextSlide="nextSlide"
      v-if="slideCurrent === 7"></Location>
    <SettingUp v-if="slideCurrent === 8"></SettingUp>
  </div>
</template>

<script>
/* eslint-disable */
import Introduction from '@/components/app/onboarding/Introduction.vue';
import SingleChoice from '@/components/app/onboarding/SingleChoice.vue';
import MultipleChoice from '@/components/app/onboarding/MultipleChoice.vue';
import MainAndSecondaryImagesUpload from '@/components/app/onboarding/MainAndSecondaryImagesUpload.vue';
import Textblock from '@/components/app/onboarding/Textblock.vue';
import Location from "@/components/app/onboarding/Location.vue";
import SettingUp from "@/components/app/onboarding/SettingUp.vue";

export default {
  components: {
    Introduction,
    SingleChoice,
    MultipleChoice,
    MainAndSecondaryImagesUpload,
    Textblock,
    Location,
    SettingUp,
  },
  data: () => ({
    slideCurrent: 0,
    slideCount: 7,
    userData: {},
    userUploadedImagesCount: 0,
  }),
  methods: {
    saveInput(...args) {
      let [key, value] = args;
      if (key === 'birthdate') {
        value = this.formatBirthdate(value);
      } else if (key === 'location') {
        value = this.processLocation(value);
      }
      this.userData[key] = value;
      this.nextSlide();
    },
    async nextSlide() {
      if (this.slideCurrent === this.slideCount) {
        this.slideCurrent += 1;
        await this.$http.post('/profile/complete', this.userData);
        await this.$http.get('/recommendations');
        await this.$store.dispatch('profileCompleted');
        await this.$router.push('/browse');
      }
      if (this.slideCurrent < this.slideCount) {
        if (this.slideCurrent === 4 && this.userUploadedImagesCount) {
          this.slideCurrent += 2;
        } else {
          this.slideCurrent += 1;
        }
      }
    },
    generateAllowedAge() {
      const ages = [];
      for (let i = 18; i < 100; i += 1) {
        ages.push(i);
      }
      return ages;
    },
    formatBirthdate(age) {
      let birthyear = new Date().getFullYear() - age;
      return '01/01/' + birthyear;
    },
    processLocation(allowAccessToLocation) {
      if (allowAccessToLocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          console.log(position.coords.latitude + position.coords.longitude);
        });
      }
    }
  },
  computed: {
    buttonText() {
      if (this.slideCurrent === 0) {
        return 'Let\'s go';
      }
      if (this.slideCurrent < this.slideCount) {
        return 'Continue';
      }
      return 'Finish';
    },
  },
  async beforeMount() {
    const response = await this.$http.get('/profile/images');
    const { images } = response.data;
    this.userUploadedImagesCount = images.length;
  },
};

</script>
