<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <div v-if="!recommendationsAnalysisDone && !sliderValuesFetched" class="mx-auto flex items-center justify-center mt-32">
      <img class="h-36" src="../../assets/loading.svg">
    </div>
    <section v-if="recommendationsAnalysisDone" class="mx-auto">
      <div class="sort-button rounded-md text-lg lg:text-2xl w-24 ml-auto" v-on:click="searchAgain()">
        <h1 class="noSelect capitalize">←</h1>
      </div>
      <Recommendations
        v-bind:showCount="showCount"
        v-on:reset-show-count="resetShowCount()"
        v-bind:title="'Potential matches'"
        v-bind:recommendationsReceived="recommendations"
        v-bind:recommendationsAnalysis="filters"></Recommendations>
    </section>
    <div id="invisibleFooterSearch" class="h-4 w-full bg-white"></div>
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
        <h1 v-if="!submitted" v-on:click="search()" class="onboarding-sub-container-content-button-outline w-48 text-lg font-normal max-w-full bg-purple-matcha w-full text-white-matcha mx-auto">
          Search</h1>
        <div v-else class="flex items-center justify-center mt-4">
          <img class="h-12" src="../../assets/loading.svg">
        </div>
      </div>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */
import FilterSlider from '@/components/shared/FilterSlider.vue';
import MultipleFilters from '@/components/shared/MultipleFilters.vue';
import Recommendations from '@/components/app/recommendations/Recommendations.vue';

export default {
  name: 'Search',
  components: {
    MultipleFilters,
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
        max: 1,
      },
      popularity: {
        min: null,
        max: null,
      },
      interests: [],
    },
    recommendationsAnalysisDone: false,
    error: null,
    submitted: false,
    showCount: 10,
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
    async fetchUsersOverfiew() {
      const sliderRangesRequest = await this.$http.get('/search/values');
      const values = sliderRangesRequest.data.search_minmax;
      this.sliders.age.min = values.min_age;
      this.filters.age.min = values.min_age;
      if (this.sliders.age.min < 18) {
        this.sliders.age.min = 18;
        this.filters.age.min = 18;
      }
      this.sliders.age.max = values.max_age;
      this.filters.age.max = values.max_age;
      this.sliders.popularity.min = values.min_score;
      this.filters.popularity.min = values.min_score;
      this.sliders.popularity.max = values.max_score;
      this.filters.popularity.max = values.max_score;
      this.sliderValuesFetched = true;
    },
    async search() {
      this.submitted = true;
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
        this.submitted = false;
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
      this.submitted = false;
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
      this.showCount = 10;
    },
    setError(message) {
      this.error = message;
    },
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    handleIntersect(entries) {
      if (entries[0].isIntersecting && this.recommendationsAnalysisDone) {
        this.showCount += 10;
      }
    },
    resetShowCount() {
      this.showCount = 10;
    },
  },
  async mounted() {
    await this.fetchUsersOverfiew();
    const options = {
      root: null,
      rootMargins: '0px',
      threshold: 0.5,
    };
    const observer = new IntersectionObserver(this.handleIntersect, options);
    observer.observe(document.querySelector('#invisibleFooterSearch'));
  },
  deactivated() {
    if (!this.$route.path.startsWith('/users')) {
      this.searchAgain();
      this.fetchUsersOverfiew();
      this.$el.scrollTop = 0;
    }
  },
};

</script>

<style scoped>
.home {
  height: calc(100% - 4rem - 2rem);
}
</style>
