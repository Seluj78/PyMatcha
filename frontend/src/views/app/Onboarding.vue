<template>
  <!-- eslint-disable max-len -->
  <div class="onboarding-container">
    <section class="onboarding-sub-container" v-if="slideCurrent === 0">
      <h1 class="onboarding-sub-container-content-heading text-8xl introduction mb-8 text-center leading-none">Meet<br>your<br>lover</h1>
      <button class="onboarding-sub-container-content-button-outline w-1/2 mt-0" v-on:click="nextSlide(0)">{{buttonText}}</button>
    </section>
    <SlideOne v-bind:slide="{current: slideCurrent, count: slideCount, buttonText}"
           v-on:saveInput="saveInput" v-if="slideCurrent === 1"></SlideOne>
    <SlideTwo v-bind:slide="{current: slideCurrent, count: slideCount, buttonText}"
              v-on:saveInput="saveInput" v-if="slideCurrent === 2"></SlideTwo>
    <SlideThree v-bind:slide="{current: slideCurrent, count: slideCount, buttonText}"
              v-on:saveInput="saveInput" v-if="slideCurrent === 3"></SlideThree>
    <SlideFour v-bind:slide="{current: slideCurrent, count: slideCount, buttonText}"
               v-on:saveInput="saveInput" v-if="slideCurrent === 4"></SlideFour>
    <SlideFive v-bind:slide="{current: slideCurrent, count: slideCount, buttonText}"
              v-on:saveInput="saveInput" v-if="slideCurrent === 5"></SlideFive>
  </div>
</template>

<script>
import SlideOne from '@/components/app/onboarding/SlideOne.vue';
import SlideTwo from '@/components/app/onboarding/SlideTwo.vue';
import SlideThree from '@/components/app/onboarding/SlideThree.vue';
import SlideFour from '@/components/app/onboarding/SlideFour.vue';
import SlideFive from '@/components/app/onboarding/SlideFive.vue';

export default {
  components: {
    SlideOne,
    SlideTwo,
    SlideThree,
    SlideFour,
    SlideFive,
  },
  data: () => ({
    slideCurrent: 0,
    slideCount: 5,
    slide1: {},
  }),
  methods: {
    saveInput(...args) {
      const [slide, value, skip] = args;
      this[slide] = value;
      this.nextSlide(skip);
    },
    nextSlide(skip) {
      if (this.slideCurrent === this.slideCount) {
        this.$router.push('/browse');
      }
      if (this.slideCurrent < this.slideCount) {
        this.slideCurrent += (1 + skip);
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

<style scoped>
.introduction {
  background: linear-gradient(315deg, #ad1deb 0%, #6e72fc 74%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.upload-small {
  height: 50%;
}
</style>
