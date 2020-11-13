<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <section class="mx-auto">
      <div v-if="!recommendationsAnalysisDone" class="flex items-center justify-center mt-32">
        <img class="h-36" src="../../assets/loading.svg">
      </div>
      <Recommendations
        v-if="recommendationsAnalysisDone"
        v-bind:showCount="showCount"
        v-on:reset-show-count="resetShowCount()"
        v-bind:title="'Potential matches'"
        v-bind:recommendationsReceived="recommendations"
        v-bind:recommendationsAnalysis="recommendationsAnalysis"></Recommendations>
      <div id="invisibleFooter" class="h-4 w-full bg-white"></div>
      <ScrollUpButton></ScrollUpButton>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */

import Recommendations from '@/components/app/recommendations/Recommendations.vue';
import ScrollUpButton from '@/components/shared/ScrollUpButton.vue';

export default {
  name: 'Browse',
  props: ['recommendationsFromSettingUp'],
  components: {
    Recommendations,
    ScrollUpButton,
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
    showCount: 10,
  }),
  methods: {
    async fetchUsers() {
      if (this.recommendationsFromSettingUp) {
        this.recommendations = this.recommendationsFromSettingUp;
      } else {
        const recommendationsRequest = await this.$http.get('/recommendations');
        this.recommendations = recommendationsRequest.data.recommendations;
      }
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
      this.showCount = 10;
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
  async created() {
    await this.fetchUsers();
  },
  mounted() {
    const options = {
      root: null,
      rootMargins: '0px',
      threshold: 0.5,
    };
    const observer = new IntersectionObserver(this.handleIntersect, options);
    observer.observe(document.querySelector('#invisibleFooter'));
  },
  deactivated() {
    if (!this.$route.path.startsWith('/users')) {
      this.browseAgain();
      this.fetchUsers();
      this.$el.scrollTop = 0;
    }
  },
};

</script>
