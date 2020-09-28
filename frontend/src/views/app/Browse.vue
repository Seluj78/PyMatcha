<template>
  <!-- eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Browse'"></NavBar>
    <section class="mx-auto">
      <Recommendations
        v-bind:title="'Potential matches'"
        v-bind:recommendations="recommendations"></Recommendations>
    </section>
  </div>
</template>

<script>
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
  }),
  async created() {
    if (this.recommendationsFromSettingUp) {
      this.recommendations = this.recommendationsFromSettingUp;
    } else {
      const recommendationsRequest = await this.$http.get('/recommendations');
      this.recommendations = recommendationsRequest.data.recommendations;
    }
  },
};

</script>
