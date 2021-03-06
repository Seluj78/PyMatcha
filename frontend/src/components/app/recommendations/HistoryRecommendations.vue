<template>
  <!-- eslint-disable max-len -->
  <section class="mb-4 sm:mb-16 lg:mb-32">
    <div v-if="recommendationsBackup.length" v-bind:class="{
      'flex': true,
      'w-full': true,
      'items-stretch': true,
      'sm:items-center': true,
      'justify-center': true,
      'md:justify-start': true,
      'mb-12': recommendationsBackup.length > 1,
      'mb-6': recommendationsBackup.length === 1,
      'relative': true}">
      <Sort
        v-if="recommendationsBackup.length > 1"
        v-bind:position="getPosition('left')"
        v-bind:startingOption="'Closest'"
        v-bind:options="['Closest', 'Furthest', 'Youngest',
        'Oldest', 'Most popular', 'Least popular', 'Most common interests', 'Least common interests']"
        v-on:save-sort="saveSort"></Sort>
      <FilterSliderDropdown
        v-if="recommendationsBackup.length > 1 && recommendationsAnalysis.age.min !== recommendationsAnalysis.age.max"
        v-bind:min="recommendationsAnalysis.age.min"
        v-bind:max="recommendationsAnalysis.age.max"
        v-bind:name="'age'"
        v-on:save-filter="saveFilter"></FilterSliderDropdown>
      <FilterSliderDropdown
        v-if="recommendationsBackup.length > 1 && recommendationsAnalysis.distance.min !== recommendationsAnalysis.distance.max"
        v-bind:min="recommendationsAnalysis.distance.min"
        v-bind:max="recommendationsAnalysis.distance.max"
        v-bind:unit="'km'"
        v-bind:name="'distance'"
        v-on:save-filter="saveFilter"></FilterSliderDropdown>
      <FilterSliderDropdown
        v-if="recommendationsBackup.length > 1 && recommendationsAnalysis.popularity.min !== recommendationsAnalysis.popularity.max"
        v-bind:min="recommendationsAnalysis.popularity.min"
        v-bind:max="recommendationsAnalysis.popularity.max"
        v-bind:unit="'pts'"
        v-bind:name="'popularity'"
        v-on:save-filter="saveFilter"></FilterSliderDropdown>
      <MultipleFiltersDropdown
        v-if="recommendationsBackup.length > 1"
        v-bind:position="getPosition('right')"
        v-bind:options="recommendationsAnalysis.interests"
        v-bind:name="'interests'"
        v-on:save-filter-multiple="saveFilterMultiple"></MultipleFiltersDropdown>
    </div>
    <div v-if="recommendations.length" ref="recommendationCards" class="grid grid-cols-1 md:grid-cols-2 gap-2">
      <RecommendationCard
        v-for="(recommendation, index) in recommendations" :key="index"
        v-bind:index="index"
        v-bind:showCount="showCount"
        v-bind:recommendation="recommendation"></RecommendationCard>
    </div>
    <div class="text-center md:text-left px-4 md:px-0" v-if="!recommendations.length">
      <h1 style="opacity: 0.085; font-size: 10vh;" class="uppercase leading-none">"Some things</h1>
      <h1 style="opacity: 0.085; font-size: 10vh;" class="uppercase leading-none">take time"</h1>
    </div>
  </section>
</template>

<script>
/* eslint-disable */
import Sort from '@/components/shared/Sort.vue';
import FilterSliderDropdown from '@/components/shared/FilterSliderDropdown.vue';
import RecommendationCard from '@/components/app/recommendations/RecommendationCard.vue';
import MultipleFiltersDropdown from '@/components/shared/MultipleFiltersDropdown.vue';

export default {
  props: ['title', 'recommendationsReceived', 'recommendationsAnalysis', 'showCount'],
  components: {
    Sort,
    RecommendationCard,
    FilterSliderDropdown,
    MultipleFiltersDropdown,
  },
  data: () => ({
    recommendations: [],
    recommendationsBackup: [],
    sorting: 'Closest',
    filters: {
      age: {
        min: null,
        max: null,
      },
      distance: {
        min: null,
        max: null,
      },
      popularity: {
        min: null,
        max: null,
      },
      interests: [],
    },
  }),
  methods: {
    getPosition(initialPosition) {
      if (this.recommendationsBackup.length > 1
      && this.recommendationsAnalysis.age.min !== this.recommendationsAnalysis.age.max
      && this.recommendationsAnalysis.distance.min !== this.recommendationsAnalysis.distance.max
      && this.recommendationsAnalysis.popularity.min !== this.recommendationsAnalysis.popularity.max) {
        return initialPosition;
      }
      return null;
    },
    saveSort(...args) {
      const [by] = args;
      this.sorting = by;
    },
    saveFilter(...range) {
      const [name, min, max] = range;
      this.filters[name].min = min;
      this.filters[name].max = max;
      this.$emit('reset-show-count');
    },
    saveFilterMultiple(...multiple) {
      const [name, filters] = multiple;
      this.filters[name] = filters;
      this.$emit('reset-show-count');
    },
    sort(recommendations, by) {
      if (by === 'Closest') {
        recommendations.sort((a, b) => a.distance - b.distance);
      } else if (by === 'Furthest') {
        recommendations.sort((a, b) => b.distance - a.distance);
      } else if (by === 'Youngest') {
        recommendations.sort((a, b) => a.age - b.age);
      } else if (by === 'Oldest') {
        recommendations.sort((a, b) => b.age - a.age);
      } else if (by === 'Most popular') {
        recommendations.sort((a, b) => b.heat_score - a.heat_score);
      } else if (by === 'Least popular') {
        recommendations.sort((a, b) => a.heat_score - b.heat_score);
      } else if (by === 'Most common interests') {
        recommendations.sort((a, b) => b.common_tags.length - a.common_tags.length);
      } else if (by === 'Least common interests') {
        recommendations.sort((a, b) => a.common_tags.length - b.common_tags.length);
      }
    },
    filter(recommendations) {
      let i = recommendations.length;
      while (i--) {
        if (!this.meetsFilters(recommendations[i])) {
          recommendations.splice(i, 1);
        }
      }
      return recommendations;
    },
    meetsFilters(recommendation) {
      return this.meetsAge(recommendation)
        && this.meetsPopularity(recommendation)
        && this.meetsDistance(recommendation)
        && this.meetsInterests(recommendation);
    },
    meetsAge(recommendation) {
      return recommendation.age >= this.filters.age.min
        && recommendation.age <= this.filters.age.max;
    },
    meetsPopularity(recommendation) {
      return recommendation.heat_score >= this.filters.popularity.min
        && recommendation.heat_score <= this.filters.popularity.max;
    },
    meetsDistance(recommendation) {
      return recommendation.distance >= this.filters.distance.min
        && recommendation.distance <= this.filters.distance.max;
    },
    meetsInterests(recommendation) {
      const recommendationInterests = recommendation.interests;
      const filterInterests = this.filters.interests;
      for (let i = 0; i < filterInterests.length; i += 1) {
        if (recommendationInterests.indexOf(filterInterests[i]) === -1) {
          return false;
        }
      }
      return true;
    },
    saveSingleChoice(...args) {
      const [key, value] = args;
      if (key === 'history') {
        this.$emit('update-history', value);
      }
    },
    setupRecommendations() {
      this.recommendations = this.recommendationsReceived;
      this.recommendationsBackup = this.recommendations;
      this.filters.age.min = this.recommendationsAnalysis.age.min;
      this.filters.age.max = this.recommendationsAnalysis.age.max;
      this.filters.distance.min = this.recommendationsAnalysis.distance.min;
      this.filters.distance.max = this.recommendationsAnalysis.distance.max;
      this.filters.popularity.min = this.recommendationsAnalysis.popularity.min;
      this.filters.popularity.max = this.recommendationsAnalysis.popularity.max;
    },
  },
  watch: {
    sorting: {
      handler() {
        this.sort(this.recommendations, this.sorting);
      },
    },
    filters: {
      handler() {
        let base = this.recommendationsBackup.slice();
        base = this.filter(base);
        this.sort(base, this.sorting);
        this.recommendations = base;
        this.$emit('filtered-count', this.recommendations.length);
      },
      deep: true,
    },
  },
  beforeMount() {
    this.setupRecommendations();
  },
};
</script>
