<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1>{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">Interests</h1>
    <p class="mt-2">{{interestsSelected}} / {{maxInterests}}</p>
    <div class="h-64 pb-1 my-8 border-b-2 max-w-xs border-purple-matcha flex flex-col items-center w-full overflow-scroll">
      <SelectionButton v-for="interest in interests" :key="interest._id" v-bind:val="interest" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
    </div>
    <button v-bind:disabled="!optionSelected.length" v-bind:class="{'onboarding-sub-container-slide-button': true, 'opacity-25': !optionSelected.length, 'cursor-default': !optionSelected.length}" v-on:click="saveInput()">{{slide.buttonText}}</button>
  </section>
</template>

<script>
import Vue from 'vue';
import SelectionButton from '@/components/app/onboarding/SelectionButton.vue';

export default {
  components: {
    SelectionButton,
  },
  props: ['slide'],
  data: () => ({
    interests: [
      'Swimming', 'Wine', 'Reading', 'Foodie',
      'Netflix', 'Music', 'Yoga', 'Golf',
      'Photography', 'Baking', 'Shopping',
      'Outdoors', 'Art', 'Travel', 'Hiking',
      'Running', 'Volunteering', 'Cycling',
      'Climbing', 'Tea', 'Fishing', 'Soccer',
      'Museum', 'Dancing', 'Surfing',
      'Karaoke', 'Grab a drink', 'DIY',
      'Walking', 'Cat lover', 'Movies',
      'Gardening', 'Trivia', 'Working out',
      'Cooking', 'Gamer', 'Brunch',
      'Blogging', 'Picknicking', 'Athlete',
      'Dog lover', 'Politics', 'Environmentalism',
      'Instagram', 'Spirituality',
      'Language exchange', 'Sports', 'Comdey',
      'Fashion', 'Disney', 'Vlogging',
      'Astrology', 'Board Games', 'Craft Beer',
      'Coffee', 'Writer',
    ],
    maxInterests: 10,
    optionSelected: [],
    bus: new Vue(),
  }),
  methods: {
    saveInput() {
      this.$emit('saveInput', 'slideThree', this.optionSelected, 0);
    },
    select(...args) {
      if (this.optionSelected.length < this.maxInterests) {
        const [val] = args;
        this.optionSelected.push(val);
      }
    },
    deselect(val) {
      this.optionSelected = this.optionSelected.filter((e) => e !== val);
    },
  },
  computed: {
    interestsSelected() {
      return this.optionSelected.length;
    },
  },
};
</script>
