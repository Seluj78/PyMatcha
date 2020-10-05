<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Search'"></NavBar>
    <section v-if="recommendationsAnalysisDone" class="mx-auto">
      <div class="sort-button rounded-md text-lg lg:text-2xl w-24 ml-auto" v-on:click="searchAgain()">
        <h1 class="noSelect capitalize">←</h1>
      </div>
      <Recommendations
        v-bind:title="'Potential matches'"
        v-bind:recommendationsReceived="recommendations"
        v-bind:recommendationsAnalysis="filters"></Recommendations>
    </section>
    <section v-if="!recommendationsAnalysisDone" class="flex flex-col my-8 md:my-12">
        <div>
          <FilterSlider
            v-bind:min="18"
            v-bind:max="100"
            v-bind:name="'age'"
            v-on:saveFilter="saveFilter"></FilterSlider>
          <FilterSlider
            v-bind:min="0"
            v-bind:max="1000"
            v-bind:unit="'km'"
            v-bind:oneHandle="true"
            v-bind:name="'distance'"
            v-on:saveFilter="saveFilter"></FilterSlider>
          <FilterSlider
            v-bind:min="18"
            v-bind:max="100"
            v-bind:unit="'pts'"
            v-bind:name="'popularity'"
            v-on:saveFilter="saveFilter"></FilterSlider>
        </div>
        <div>
          <MultipleFilters
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
            v-on:saveFilterMultiple="saveFilterMultiple"></MultipleFilters>
        </div>
      <div class="mx-auto w-full max-w-md">
        <h1 v-on:click="search()" class="onboarding-sub-container-content-button-outline w-48 text-lg font-normal max-w-full bg-purple-matcha w-full text-white-matcha mx-auto">
          Search</h1>
      </div>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */
import NavBar from '@/components/shared/NavBar.vue';
import FilterSlider from '@/components/shared/FilterSlider.vue';
import MultipleFilters from '@/components/shared/MultipleFilters.vue';
import Recommendations from '@/components/app/recommendations/Recommendations.vue';

export default {
  components: {
    MultipleFilters,
    NavBar,
    FilterSlider,
    Recommendations,
  },
  data: () => ({
    recommendations: [],
    filters: {
      age: {
        min: null,
        max: null,
      },
      distance: {
        min: 0,
        max: null,
      },
      popularity: {
        min: null,
        max: null,
      },
      interests: [],
    },
    recommendationsAnalysisDone: false,
  }),
  methods: {
    saveFilter(...range) {
      const [name, min, max, oneHandle] = range;
      if (oneHandle) {
        this.filters[name].max = min;
      } else {
        this.filters[name].min = min;
        this.filters[name].max = max;
      }
    },
    saveFilterMultiple(...multiple) {
      const [name, filters] = multiple;
      this.filters[name] = filters;
    },
    async search() {
      if (this.filters.interests.length === 0) {
        this.filters.interests = [
          'swimming', 'wine', 'reading', 'foodie', 'netflix', 'music', 'yoga', 'golf',
          'photography', 'baking', 'shopping', 'outdoors', 'art', 'travel', 'hiking',
          'running', 'volunteering', 'cycling', 'climbing', 'tea', 'fishing', 'soccer',
          'museum', 'dancing', 'surfing', 'karaoke', 'parties', 'diy',
          'walking', 'cat lover', 'movies', 'gardening', 'trivia', 'working out',
          'cooking', 'gamer', 'brunch', 'blogging', 'picknicking', 'athlete',
          'dog lover', 'politics', 'environmentalism', 'instagram', 'spirituality',
          'language exchange', 'sports', 'comedy', 'fashion', 'disney', 'vlogging',
          'astrology', 'board games', 'craft beer', 'coffee', 'writer',
        ];
      }
      const searchRequest = await this.$http.post('/search', {
        min_age: this.filters.age.min,
        max_age: this.filters.age.max,
        min_score: this.filters.popularity.min,
        max_score: this.filters.popularity.max,
        max_distance: this.filters.distance.max,
        tags: this.filters.interests,
      });
      this.recommendations = searchRequest.data.search_results;
      this.recommendations.sort((a, b) => a.distance - b.distance);
      for (let i = 0; i < this.recommendations.length; i += 1) {
        if (this.recommendations[i].age < 18) {
          this.recommendations[i].age = 18;
        }
        const interests = this.recommendations[i].tags;
        this.recommendations[i].interests = [];
        this.recommendations[i].distance = Math.floor(this.recommendations[i].distance);
        for (let j = 0; j < interests.length; j += 1) {
          this.recommendations[i].interests.push(interests[j].name);
        }
      }
      this.recommendationsAnalysisDone = true;
    },
    searchAgain() {
      this.recommendationsAnalysisDone = false;
    },
  },
};

</script>

<style scoped>
.home {
  height: calc(100% - 4rem - 2rem);
}
</style>
