<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'History'"></NavBar>
    <section class="mx-auto mt-4">
      <div class="flex items-center justify-center md:justify-start w-full mb-4">
        <h1
          class="text-3xl sm:text-5xl my-4 inline-block text-center leading-none onboarding-sub-container-content-heading">
          {{filteredCount || 0}}</h1>
        <DropdownDisplayChoiceHistory
          v-on:save-single-choice="updateHistory"
          class="inline-block ml-4"
          v-bind:name="'history'"
          v-bind:starting-option="'People I viewed'"
          v-bind:options="['People I viewed', 'People I liked', 'Who viewed me', 'Who liked me', 'Whom I blocked']"></DropdownDisplayChoiceHistory>
      </div>
      <HistoryRecommendations
        v-if="recommendationsAnalysisDone"
        v-on:filtered-count="filteredCountSave"
        v-bind:title="'Potential matches'"
        v-bind:recommendationsReceived="recommendations"
        v-bind:recommendationsAnalysis="recommendationsAnalysis"></HistoryRecommendations>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */

import NavBar from '@/components/shared/NavBar.vue';
import HistoryRecommendations from '@/components/app/recommendations/HistoryRecommendations.vue';
import DropdownDisplayChoiceHistory from '@/components/shared/DropdownDisplayChoiceHistory.vue';

export default {
  name: 'History',
  props: ['recommendationsFromSettingUp'],
  components: {
    NavBar,
    HistoryRecommendations,
    DropdownDisplayChoiceHistory,
  },
  data: () => ({
    recommendations: [],
    recommendationsAnalysis: {
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
    recommendationsAnalysisDone: false,
    filteredCount: null,
  }),
  methods: {
    async fetchUsers(request) {
      if (request === 'People I viewed') {
        const recommendationsRequest = await this.$http.get('/history/viewed');
        this.recommendations = recommendationsRequest.data.viewed;
      } else if (request === 'People I liked') {
        const recommendationsRequest = await this.$http.get('/history/liked');
        this.recommendations = recommendationsRequest.data.liked;
      } else if (request === 'Who viewed me') {
        const recommendationsRequest = await this.$http.get('/history/viewed/me');
        this.recommendations = recommendationsRequest.data.viewed_me;
      } else if (request === 'Who liked me') {
        const recommendationsRequest = await this.$http.get('/history/liked/me');
        this.recommendations = recommendationsRequest.data.liked_me;
      } else if (request === 'Whom I blocked') {
        const recommendationsRequest = await this.$http.get('/history/blocked');
        this.recommendations = recommendationsRequest.data.bloked;
      }
      this.recommendations = Object.values(this.recommendations.reduce((acc, cur) => Object.assign(acc, { [cur.id]: cur }), {}));
      this.recommendations.sort((a, b) => a.distance - b.distance);
      for (let i = 0; i < this.recommendations.length; i += 1) {
        this.recommendations[i].distance = Math.floor(this.recommendations[i].distance);
        if (this.recommendations[i].age < 18) {
          this.recommendations[i].age = 18;
        }
        if (this.recommendationsAnalysis.age.min === null || this.recommendations[i].age < this.recommendationsAnalysis.age.min) {
          this.recommendationsAnalysis.age.min = this.recommendations[i].age;
        }
        if (this.recommendationsAnalysis.age.max === null || this.recommendations[i].age > this.recommendationsAnalysis.age.max) {
          this.recommendationsAnalysis.age.max = this.recommendations[i].age;
        }
        if (this.recommendationsAnalysis.distance.min === null || this.recommendations[i].distance < this.recommendationsAnalysis.distance.min) {
          this.recommendationsAnalysis.distance.min = this.recommendations[i].distance;
        }
        if (this.recommendationsAnalysis.distance.max === null || this.recommendations[i].distance > this.recommendationsAnalysis.distance.max) {
          this.recommendationsAnalysis.distance.max = this.recommendations[i].distance;
        }
        if (this.recommendationsAnalysis.popularity.min === null || this.recommendations[i].heat_score < this.recommendationsAnalysis.popularity.min) {
          this.recommendationsAnalysis.popularity.min = this.recommendations[i].heat_score;
        }
        if (this.recommendationsAnalysis.popularity.max === null || this.recommendations[i].heat_score > this.recommendationsAnalysis.popularity.max) {
          this.recommendationsAnalysis.popularity.max = this.recommendations[i].heat_score;
        }
        const interests = this.recommendations[i].tags;
        this.recommendations[i].interests = [];
        for (let j = 0; j < interests.length; j += 1) {
          this.recommendations[i].interests.push(interests[j].name);
          if (this.recommendationsAnalysis.interests.indexOf(interests[j].name) === -1) {
            this.recommendationsAnalysis.interests.push(interests[j].name);
          }
        }
      }
      this.recommendationsAnalysisDone = true;
    },
    browseAgain() {
      this.recommendations = [];
      this.recommendationsAnalysis.age.min = null;
      this.recommendationsAnalysis.age.max = null;
      this.recommendationsAnalysis.distance.min = null;
      this.recommendationsAnalysis.distance.max = null;
      this.recommendationsAnalysis.popularity.min = null;
      this.recommendationsAnalysis.popularity.max = null;
      this.recommendationsAnalysis.interests = [];
      this.recommendationsAnalysisDone = false;
    },
    updateHistory(...args) {
      const [key, value] = args;
      if (key === 'history') {
        this.browseAgain();
        this.fetchUsers(value);
        this.filteredCount = this.recommendations.count;
      }
    },
    filteredCountSave(...args) {
      const [count] = args;
      this.filteredCount = count;
    },
  },
  async created() {
    await this.fetchUsers('People I viewed');
    this.filteredCount = this.recommendations.length;
  },
  deactivated() {
    if (!this.$route.path.startsWith('/users')) {
      this.browseAgain();
      this.fetchUsers('People I viewed');
      this.$el.scrollTop = 0;
    }
  },
};

</script>
