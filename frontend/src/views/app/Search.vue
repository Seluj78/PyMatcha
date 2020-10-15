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
    <section v-on:click="setError(null)"
             v-if="!recommendationsAnalysisDone && sliderValuesFetched"
             class="flex flex-col my-8 md:my-12">
        <div><img src="../../assets/search.png" class="w-20 mb-4 mx-auto"></div>
        <div>
          <FilterSlider
            v-bind:min="sliders.age.min"
            v-bind:max="sliders.age.max"
            v-bind:name="'age'"
            v-on:save-filter="saveFilter"></FilterSlider>
          <FilterSlider
            v-bind:min="1"
            v-bind:max="2000"
            v-bind:unit="'km'"
            v-bind:oneHandle="true"
            v-bind:name="'distance'"
            v-on:save-filter="saveFilter"></FilterSlider>
          <FilterSlider
            v-bind:min="sliders.popularity.min"
            v-bind:max="sliders.popularity.max"
            v-bind:unit="'pts'"
            v-bind:name="'popularity'"
            v-on:save-filter="saveFilter"></FilterSlider>
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
            v-bind:info="'If no selected, all are accounted.'"
            v-on:save-filter-multiple="saveFilterMultiple"></MultipleFilters>
        </div>
      <div class="auth-sub-container-error mx-auto max-w-md" v-if="error"><h1 class="auth-sub-container-error-message">{{ error }}</h1></div>
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
    sliders: {
      age: {
        min: null,
        max: null,
      },
      popularity: {
        min: null,
        max: null,
      },
    },
    sliderValuesFetched: false,
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
    error: null,
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
      const searchRequest = await this.$http.post('/search', {
        min_age: this.filters.age.min,
        max_age: this.filters.age.max,
        min_score: this.filters.popularity.min,
        max_score: this.filters.popularity.max,
        max_distance: this.filters.distance.max,
        tags: this.filters.interests,
      });
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
      this.recommendations = searchRequest.data.search_results;
      if (this.recommendations.length === 0) {
        this.setError('0 profiles found. Please, try expanding your search criteria.');
        return;
      }
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
      this.scrollToTop();
    },
    searchAgain() {
      this.filters.age.min = null;
      this.filters.age.max = null;
      this.filters.popularity.min = null;
      this.filters.popularity.max = null;
      this.filters.distance.max = null;
      this.filters.interests = [];
      this.recommendationsAnalysisDone = false;
    },
    setError(message) {
      this.error = message;
    },
    scrollToTop() {
      window.scrollTo(0, 0);
    },
  },
  async mounted() {
    const sliderRangesRequest = await this.$http.get('/search/values');
    const values = sliderRangesRequest.data.search_minmax;
    this.sliders.age.min = values.min_age;
    if (this.sliders.age.min < 18) {
      this.sliders.age.min = 18;
    }
    this.sliders.age.max = values.max_age;
    this.sliders.popularity.min = values.min_score;
    this.sliders.popularity.max = values.max_score;
    this.sliderValuesFetched = true;
  },
};

</script>

<style scoped>
.home {
  height: calc(100% - 4rem - 2rem);
}
</style>
