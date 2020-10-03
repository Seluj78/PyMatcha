<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Search'"></NavBar>
    <section v-if="searchSubmitted">results</section>
    <section v-if="!searchSubmitted" class="flex flex-col my-8 md:my-12">
        <div>
          <FilterSlider
            v-bind:min="18"
            v-bind:max="100"
            v-bind:name="'age'"
            v-on:saveFilter="saveFilter"></FilterSlider>
          <FilterSlider
            v-bind:min="18"
            v-bind:max="100"
            v-bind:name="'distance'"
            v-on:saveFilter="saveFilter"></FilterSlider>
          <FilterSlider
            v-bind:min="18"
            v-bind:max="100"
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

export default {
  props: ['recommendationsFromSettingUp'],
  components: {
    MultipleFilters,
    NavBar,
    FilterSlider,
  },
  data: () => ({
    searchSubmitted: false,
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
    saveFilter(...range) {
      const [name, min, max] = range;
      this.filters[name].min = min;
      this.filters[name].max = max;
    },
    saveFilterMultiple(...multiple) {
      const [name, filters] = multiple;
      this.filters[name] = filters;
    },
    search() {
      this.searchSubmitted = true;
    },
  },
};

</script>

<style scoped>
.home {
  height: calc(100% - 4rem - 2rem);
}
</style>
