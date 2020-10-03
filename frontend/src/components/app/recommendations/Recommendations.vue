<template>
  <!-- eslint-disable max-len -->
  <section>
    <h1
      class="text-5xl my-4 text-center md:text-left leading-none onboarding-sub-container-content-heading">
      {{recommendations.length}} {{title}}</h1>
    <div class="flex w-full items-stretch sm:items-center justify-center md:justify-start mb-12 relative">
      <Sort
        v-bind:position="'left'"
        v-bind:startingOption="'Closest'"
        v-bind:options="['Closest', 'Furthest', 'Youngest',
        'Oldest', 'Most popular', 'Least popular', 'Most common interests', 'Least common interests']"
        v-on:saveSort="saveSort"></Sort>
      <FilterSliderDropdown
        v-bind:min="recommendationsAnalysis.age.min"
        v-bind:max="recommendationsAnalysis.age.max"
        v-bind:name="'age'"
        v-on:saveFilter="saveFilter"></FilterSliderDropdown>
      <FilterSliderDropdown
        v-bind:min="recommendationsAnalysis.distance.min"
        v-bind:max="recommendationsAnalysis.distance.max"
        v-bind:unit="'km'"
        v-bind:name="'distance'"
        v-on:saveFilter="saveFilter"></FilterSliderDropdown>
      <FilterSliderDropdown
        v-bind:min="recommendationsAnalysis.popularity.min"
        v-bind:max="recommendationsAnalysis.popularity.max"
        v-bind:unit="'pts'"
        v-bind:name="'popularity'"
        v-on:saveFilter="saveFilter"></FilterSliderDropdown>
      <MultipleFiltersDropdown
        v-bind:position="'right'"
        v-bind:options="recommendationsAnalysis.uniqueInterests"
        v-bind:name="'interests'"
        v-on:saveFilterMultiple="saveFilterMultiple"></MultipleFiltersDropdown>
    </div>
    <div ref="recommendationCards" class="grid grid-cols-1 md:grid-cols-2 gap-2">
    <RecommendationCard
      v-for="(recommendation, index) in recommendations" :key="index"
      v-bind:recommendation="recommendation"></RecommendationCard>
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
  props: ['title', 'recommendationsReceived', 'recommendationsAnalysis'],
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
    saveSort(...args) {
      const [by] = args;
      this.sorting = by;
    },
    saveFilter(...range) {
      const [name, min, max] = range;
      this.filters[name].min = min;
      this.filters[name].max = max;
    },
    saveFilterMultiple(...multiple) {
      const [name, filters] = multiple;
      this.filters[name] = filters;
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
      },
      deep: true,
    }
  },
  beforeMount() {
    this.recommendations = this.recommendationsReceived;
    this.recommendationsBackup = this.recommendationsReceived;
    this.filters.age.min = this.recommendationsAnalysis.age.min;
    this.filters.age.max = this.recommendationsAnalysis.age.max;
    this.filters.distance.min = this.recommendationsAnalysis.distance.min;
    this.filters.distance.max = this.recommendationsAnalysis.distance.max;
    this.filters.popularity.min = this.recommendationsAnalysis.popularity.min;
    this.filters.popularity.max = this.recommendationsAnalysis.popularity.max;
  }
};
</script>
