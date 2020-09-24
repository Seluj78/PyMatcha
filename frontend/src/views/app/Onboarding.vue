<template>
  <!-- eslint-disable max-len -->
  <div class="onboarding-container">
    <Introduction
      v-bind:slide="{buttonText}"
      v-on:nextSlide="nextSlide"
      v-if="slideCurrent === 0"></Introduction>
    <SingleChoice
      v-bind:slide="{
      key: 'gender',
      current: slideCurrent,
      count: slideCount,
      header: 'I am',
      options: ['Male', 'Female', 'Other'],
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 1"></SingleChoice>
    <SingleChoice
      v-bind:slide="{
      key: 'orientation',
      current: slideCurrent,
      count: slideCount,
      header: 'Sexuality',
      options: ['Heterosexual', 'Homosexual', 'Bi-sexual', 'Other'],
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 2"></SingleChoice>
    <MultipleChoice
      v-bind:slide="{
      key: 'interests' ,
      current: slideCurrent,
      count: slideCount,
      header: 'Interests',
      options: [
        'Swimming', 'Wine', 'Reading', 'Foodie', 'Netflix', 'Music', 'Yoga', 'Golf',
        'Photography', 'Baking', 'Shopping', 'Outdoors', 'Art', 'Travel', 'Hiking',
        'Running', 'Volunteering', 'Cycling', 'Climbing', 'Tea', 'Fishing', 'Soccer',
        'Museum', 'Dancing', 'Surfing', 'Karaoke', 'Grab a drink', 'DIY',
        'Walking', 'Cat lover', 'Movies', 'Gardening', 'Trivia', 'Working out',
        'Cooking', 'Gamer', 'Brunch', 'Blogging', 'Picknicking', 'Athlete',
        'Dog lover', 'Politics', 'Environmentalism', 'Instagram', 'Spirituality',
        'Language exchange', 'Sports', 'Comdey', 'Fashion', 'Disney', 'Vlogging',
        'Astrology', 'Board Games', 'Craft Beer', 'Coffee', 'Writer',
      ],
      minOptionsForSelection: 3,
      maxOptionsForSelection: 10,
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 3"></MultipleChoice>
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
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 4"></MainAndSecondaryImagesUpload>
    <Textblock
      v-bind:slide="{
      key: 'bio',
      current: slideCurrent,
      count: slideCount,
      minTextareaLength: 50,
      maxTextareaLength: 200,
      placeholder: 'I am best described as ...',
      buttonText}"
      v-on:saveInput="saveInput"
      v-if="slideCurrent === 5"></Textblock>
  </div>
</template>

<script>
import Introduction from '@/components/app/onboarding/Introduction.vue';
import SingleChoice from '@/components/app/onboarding/SingleChoice.vue';
import MultipleChoice from '@/components/app/onboarding/MultipleChoice.vue';
import MainAndSecondaryImagesUpload from '@/components/app/onboarding/MainAndSecondaryImagesUpload.vue';
import Textblock from '@/components/app/onboarding/Textblock.vue';

export default {
  components: {
    Introduction,
    SingleChoice,
    MultipleChoice,
    MainAndSecondaryImagesUpload,
    Textblock,
  },
  data: () => ({
    slideCurrent: 0,
    slideCount: 5,
    userData: {},
  }),
  methods: {
    saveInput(...args) {
      const [key, value] = args;
      this.userData[key] = value;
      console.log(this.userData);
      this.nextSlide();
    },
    nextSlide() {
      if (this.slideCurrent === this.slideCount) {
        this.$router.push('/browse');
      }
      if (this.slideCurrent < this.slideCount) {
        this.slideCurrent += 1;
      }
    },
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
};

</script>
