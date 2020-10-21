<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'History'"></NavBar>
    <section class="mx-auto">
      <HistoryRecommendations
        v-if="firstTimeAnalysisDone"
        v-bind:ready="recommendationsAnalysisDone"
        v-on:update-history="updateHistory"
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

export default {
  name: 'History',
  props: ['recommendationsFromSettingUp'],
  components: {
    NavBar,
    HistoryRecommendations,
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
    firstTimeAnalysisDone: false,
  }),
  methods: {
    async fetchUsers() {
      const recommendationsRequest = await this.$http.get('/recommendations');
      this.recommendations = recommendationsRequest.data.recommendations;
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
      this.firstTimeAnalysisDone = true;
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
      const [request] = args;
      if (request === 'People I view') {
        console.log(1);
      } else if (request === 'People I like') {
        console.log(2);
      } else if (request === 'Who views me') {
        console.log(3);
      } else if (request === 'Who likes me') {
        console.log(4);
      } else if (request === 'Whom I block') {
        console.log(5);
      }
      this.browseAgain();
      this.fetchUsers();
    },
  },
  async created() {
    await this.fetchUsers();
  },
  deactivated() {
    if (!this.$route.path.startsWith('/users')) {
      this.firstTimeAnalysisDone = false;
      this.browseAgain();
      this.fetchUsers();
      this.$el.scrollTop = 0;
    }
  },
};

</script>
