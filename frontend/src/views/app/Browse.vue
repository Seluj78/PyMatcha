<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Browse'"></NavBar>
    <section class="mx-auto">
      <Recommendations
        v-if="recommendationsAnalysisDone"
        v-bind:title="'Potential matches'"
        v-bind:recommendations="recommendations"
        v-bind:recommendationsAnalysis="recommendationsAnalysis"></Recommendations>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */
import NavBar from '@/components/shared/NavBar.vue';
import Recommendations from '@/components/app/recommendations/Recommendations.vue';

export default {
  props: ['recommendationsFromSettingUp'],
  components: {
    NavBar,
    Recommendations,
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
      uniqueInterests: [],
    },
    recommendationsAnalysisDone: false,
  }),
  async created() {
    if (this.recommendationsFromSettingUp) {
      this.recommendations = this.recommendationsFromSettingUp;
    } else {
      const recommendationsRequest = await this.$http.get('/recommendations');
      this.recommendations = recommendationsRequest.data.recommendations;
    }
    this.recommendations.sort((a, b) => a.distance - b.distance);
    for (let i = 0; i < this.recommendations.length; i += 1) {
      if (this.recommendationsAnalysis.age.min === null || this.recommendations[i].age < this.recommendationsAnalysis.age.min) {
        this.recommendationsAnalysis.age.min = this.recommendations[i].age;
      }
      if (this.recommendationsAnalysis.age.max === null || this.recommendations[i].age > this.recommendationsAnalysis.age.max) {
        this.recommendationsAnalysis.age.max = this.recommendations[i].age;
      }
      if (this.recommendationsAnalysis.distance.min === null || Math.floor(this.recommendations[i].distance) < this.recommendationsAnalysis.distance.min) {
        this.recommendationsAnalysis.distance.min = Math.floor(this.recommendations[i].distance);
      }
      if (this.recommendationsAnalysis.distance.max === null || Math.floor(this.recommendations[i].distance) > this.recommendationsAnalysis.distance.max) {
        this.recommendationsAnalysis.distance.max = Math.floor(this.recommendations[i].distance);
      }
      if (this.recommendationsAnalysis.popularity.min === null || this.recommendations[i].heat_score < this.recommendationsAnalysis.popularity.min) {
        this.recommendationsAnalysis.popularity.min = this.recommendations[i].heat_score;
      }
      if (this.recommendationsAnalysis.popularity.max === null || this.recommendations[i].heat_score > this.recommendationsAnalysis.popularity.max) {
        this.recommendationsAnalysis.popularity.max = this.recommendations[i].heat_score;
      }
      const interests = this.recommendations[i].tags;
      for (let j = 0; j < interests.length; j += 1) {
        if (this.recommendationsAnalysis.uniqueInterests.indexOf(interests[j].name) === -1) {
          this.recommendationsAnalysis.uniqueInterests.push(interests[j].name);
        }
      }
    }
    this.recommendationsAnalysisDone = true;
  },
};

</script>
