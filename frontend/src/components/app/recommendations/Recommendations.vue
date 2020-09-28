<template>
  <!-- eslint-disable max-len -->
  <section>
    <h1 class="text-5xl my-4 text-center md:text-left leading-none onboarding-sub-container-content-heading">{{recommendations.length}} {{title}}</h1>
    <div class="flex w-full items-stretch sm:items-center justify-center md:justify-start mb-12 relative">
      <Sort
        v-bind:position="'left'"
        v-bind:options="['Youngest', 'Oldest', 'Closest', 'Furthest', 'Most popular', 'Least popular', 'Most common interests', 'Least common interests']"
        v-on:sort="sort"></Sort>
      <FilterSlider v-bind:name="'age'" v-on:filter="filter"></FilterSlider>
      <FilterSlider v-bind:unit="'km'" v-bind:name="'distance'" v-on:filter="filter"></FilterSlider>
      <FilterSlider v-bind:unit="'pts'" v-bind:name="'fame'" v-on:filter="filter"></FilterSlider>
      <MultipleFiltersDropdown
        v-bind:position="'right'"
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
        v-bind:name="'interests'"
        v-on:filter="filter"></MultipleFiltersDropdown>
    </div>
<!--    <div class="flex flex-wrap items-center justify-start">-->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
    <RecommendationCard
      v-for="(recommendation, index) in recommendations" :key="index"
      v-bind:recommendation="recommendation" v-bind:index="index + 1"></RecommendationCard>
    </div>
  </section>
</template>

<script>
/* eslint-disable */
import Sort from '@/components/shared/Sort.vue';
import FilterSlider from '@/components/shared/FilterSlider.vue';
import RecommendationCard from '@/components/app/recommendations/RecommendationCard.vue';
import MultipleFiltersDropdown from '@/components/shared/MultipleFiltersDropdown.vue';

export default {
  components: {
    Sort,
    RecommendationCard,
    FilterSlider,
    MultipleFiltersDropdown,
  },
  methods: {
    sort() {
      console.log('sort');
    },
    filter() {
      console.log('filter');
    },
  },
  props: ['title', 'recommendations'],
};
</script>
