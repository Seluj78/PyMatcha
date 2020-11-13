<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <div v-if="!historyFetched" class="mx-auto flex items-center justify-center mt-32">
      <img class="h-36" src="../../assets/loading.svg">
    </div>
    <section v-bind:class="{'mx-auto': true, 'mt-4': true, 'invisible': !historyFetched}">
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
        v-bind:showCount="showCount"
        v-on:reset-show-count="resetShowCount()"
        v-on:filtered-count="filteredCountSave"
        v-bind:title="'Potential matches'"
        v-bind:recommendationsReceived="recommendations"
        v-bind:recommendationsAnalysis="recommendationsAnalysis"></HistoryRecommendations>
      <div id="invisibleFooterHistory" class="h-4 w-full bg-white"></div>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */
/* eslint-disable no-param-reassign */

import HistoryRecommendations from '@/components/app/recommendations/HistoryRecommendations.vue';
import DropdownDisplayChoiceHistory from '@/components/shared/DropdownDisplayChoiceHistory.vue';

export default {
  name: 'History',
  props: ['recommendationsFromSettingUp'],
  components: {
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
    historyFetched: false,
    visitUser: false,
    showCount: 10,
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
        this.recommendations = recommendationsRequest.data.blocked;
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
      this.historyFetched = true;
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
      this.historyFetched = false;
      this.visitUser = false;
      this.showCount = 10;
    },
    async updateHistory(...args) {
      const [key, value] = args;
      if (key === 'history') {
        this.browseAgain();
        await this.fetchUsers(value);
        this.filteredCount = this.recommendations.length;
      }
    },
    filteredCountSave(...args) {
      const [count] = args;
      this.filteredCount = count;
    },
    handleIntersect(entries) {
      if (entries[0].isIntersecting) {
        this.showCount += 10;
      }
    },
    resetShowCount() {
      this.showCount = 10;
    },
  },
  mounted() {
    const options = {
      root: null,
      rootMargins: '0px',
      threshold: 0.5,
    };
    const observer = new IntersectionObserver(this.handleIntersect, options);
    observer.observe(document.querySelector('#invisibleFooterHistory'));
  },
  async beforeRouteEnter(to, from, next) {
    next(async (vm) => {
      if (from.name !== 'Users' || !vm.visitUser) {
        vm.browseAgain();
        await vm.fetchUsers('People I viewed');
        vm.filteredCount = vm.recommendations.length;
        vm.$el.scrollTop = 0;
      }
      vm.prevRoute = from;
    });
  },
  deactivated() {
    if (!this.$route.path.startsWith('/users')) {
      this.browseAgain();
      this.fetchUsers('People I viewed');
      this.$el.scrollTop = 0;
    } else {
      this.visitUser = true;
    }
  },
};

</script>
