<template>
  <!-- eslint-disable max-len -->
  <section>
    <h1 class="text-5xl my-4 text-center md:text-left leading-none onboarding-sub-container-content-heading">{{recommendations.length}} {{title}}</h1>
    <div class="flex w-full items-stretch sm:items-center justify-center md:justify-start mb-12 relative">
      <Sort
        v-bind:position="'left'"
        v-bind:options="['Closest', 'Furthest', 'Youngest', 'Oldest', 'Most popular', 'Least popular', 'Most common interests', 'Least common interests']"
        v-on:sort="sort"></Sort>
      <FilterSlider
        v-bind:min="recommendationsAnalysis.age.min"
        v-bind:max="recommendationsAnalysis.age.max"
        v-bind:name="'age'"
        v-on:filter="filter"></FilterSlider>
      <FilterSlider
        v-bind:min="recommendationsAnalysis.distance.min"
        v-bind:max="recommendationsAnalysis.distance.max"
        v-bind:unit="'km'"
        v-bind:name="'distance'"
        v-on:filter="filter"></FilterSlider>
      <FilterSlider
        v-bind:min="recommendationsAnalysis.popularity.min"
        v-bind:max="recommendationsAnalysis.popularity.max"
        v-bind:unit="'pts'"
        v-bind:name="'fame'"
        v-on:filter="filter"></FilterSlider>
      <MultipleFiltersDropdown
        v-bind:position="'right'"
        v-bind:options="recommendationsAnalysis.uniqueInterests"
        v-bind:name="'interests'"
        v-on:filter="filter"></MultipleFiltersDropdown>
    </div>
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
  props: ['title', 'recommendations', 'recommendationsAnalysis'],
  components: {
    Sort,
    RecommendationCard,
    FilterSlider,
    MultipleFiltersDropdown,
  },
  data: () => ({
    loggedInUser: null,
  }),
  methods: {
    sort(...args) {
      const [by] = args;
      if (by === 'Closest') {
        this.recommendations.sort((a, b) => a.distance - b.distance);
      } else if (by === 'Furthest') {
        this.recommendations.sort((a, b) => b.distance - a.distance);
      } else if (by === 'Youngest') {
        this.recommendations.sort((a, b) => a.age - b.age);
      } else if (by === 'Oldest') {
        this.recommendations.sort((a, b) => b.age - a.age);
      } else if (by === 'Most popular') {
        this.recommendations.sort((a, b) => b.heat_score - a.heat_score);
      } else if (by === 'Least popular') {
        this.recommendations.sort((a, b) => a.heat_score - b.heat_score);
      } else if (by === 'Most common interests') {
        this.recommendations.sort((a, b) => this.count_similarities(a.tags, this.loggedInUser.tags) - this.count_similarities(b.tags, this.loggedInUser.tags));
      } else if (by === 'Least common interests') {
        this.recommendations.sort((a, b) => this.count_similarities(b.tags, this.loggedInUser.tags) - this.count_similarities(a.tags, this.loggedInUser.tags));
      }
    },
    count_similarities(arrayA, arrayB) {
      let matches = 0;
      for (let i = 0 ; i < arrayA.length; i++) {
        if (arrayB.indexOf(arrayA[i].name) != -1) {
          matches++;
        }
      }
      return matches;
    },
    filter() {
      console.log('filter');
    },
  },
  mounted() {
    this.loggedInUser = this.$store.getters.getLoggedInUser;
  }
};
</script>
