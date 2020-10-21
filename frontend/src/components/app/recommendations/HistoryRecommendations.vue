<template>
  <!-- eslint-disable max-len -->
  <section class="mb-4 sm:mb-16 lg:mb-32">
    <div class="flex items-center justify-center md:justify-start w-full mb-4">
      <h1
        class="text-3xl sm:text-5xl my-4 inline-block text-center leading-none onboarding-sub-container-content-heading">
        {{recommendations.length}}</h1>
      <DropdownDisplayChoiceHistory
        v-on:save-single-choice="saveSingleChoice"
        class="inline-block ml-4"
        v-bind:name="'history'"
        v-bind:starting-option="'People I viewed'"
        v-bind:options="['People I view', 'People I like', 'Who views me', 'Who likes me', 'Whom I block']"></DropdownDisplayChoiceHistory>
    </div>
    <div class="flex w-full items-stretch sm:items-center justify-center md:justify-start mb-12 relative">
      <Sort
        v-bind:position="'left'"
        v-bind:startingOption="'Closest'"
        v-bind:options="['Closest', 'Furthest', 'Youngest',
        'Oldest', 'Most popular', 'Least popular', 'Most common interests', 'Least common interests']"
        v-on:save-sort="saveSort"></Sort>
      <FilterSliderDropdown
        v-bind:min="recommendationsAnalysis.age.min"
        v-bind:max="recommendationsAnalysis.age.max"
        v-bind:name="'age'"
        v-on:save-filter="saveFilter"></FilterSliderDropdown>
      <FilterSliderDropdown
        v-bind:min="recommendationsAnalysis.distance.min"
        v-bind:max="recommendationsAnalysis.distance.max"
        v-bind:unit="'km'"
        v-bind:name="'distance'"
        v-on:save-filter="saveFilter"></FilterSliderDropdown>
      <FilterSliderDropdown
        v-bind:min="recommendationsAnalysis.popularity.min"
        v-bind:max="recommendationsAnalysis.popularity.max"
        v-bind:unit="'pts'"
        v-bind:name="'popularity'"
        v-on:save-filter="saveFilter"></FilterSliderDropdown>
      <MultipleFiltersDropdown
        v-bind:position="'right'"
        v-bind:options="recommendationsAnalysis.interests"
        v-bind:name="'interests'"
        v-on:save-filter-multiple="saveFilterMultiple"></MultipleFiltersDropdown>
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
import DropdownDisplayChoiceHistory from '@/components/shared/DropdownDisplayChoiceHistory.vue';

export default {
  props: ['title', 'recommendationsReceived', 'recommendationsAnalysis'],
  components: {
    Sort,
    RecommendationCard,
    FilterSliderDropdown,
    MultipleFiltersDropdown,
    DropdownDisplayChoiceHistory,
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
    filterOutBlockedUsers(recommendations) {
      let i = recommendations.length;
      const { blocks } = this.$store.getters.getLoggedInUser;
      let blockedIds = [];
      for (let j = 0; j < blocks.length; j += 1) {
        blockedIds.push(blocks[j].blocked_id);
      }
      while (i--) {
        if (blockedIds.indexOf(recommendations[i].id) !== -1) {
          recommendations.splice(i, 1);
        }
      }
      return recommendations;
    },
    saveSingleChoice(...args) {
      const [key, value] = args;
      if (key === 'history') {
        this.$emit('update-history', value);
      }
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
    this.recommendations = this.filterOutBlockedUsers(this.recommendationsReceived);
    this.recommendationsBackup = this.recommendations;
    this.filters.age.min = this.recommendationsAnalysis.age.min;
    this.filters.age.max = this.recommendationsAnalysis.age.max;
    this.filters.distance.min = this.recommendationsAnalysis.distance.min;
    this.filters.distance.max = this.recommendationsAnalysis.distance.max;
    this.filters.popularity.min = this.recommendationsAnalysis.popularity.min;
    this.filters.popularity.max = this.recommendationsAnalysis.popularity.max;
  }
};
</script>
