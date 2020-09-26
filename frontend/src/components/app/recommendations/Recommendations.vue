<template>
  <!-- eslint-disable max-len -->
  <section>
    <h1 class="text-5xl mb-4 text-center sm:text-left onboarding-sub-container-content-heading">{{title}}</h1>
    <div class="flex flex-wrap items-center justify-start">
    <RecommendationCard
      v-for="(recommendation, index) in recommendations" :key="index"
      v-bind:recommendation="recommendation" v-bind:index="index + 1"></RecommendationCard>
    </div>
  </section>
</template>

<script>
import RecommendationCard from '@/components/app/recommendations/RecommendationCard.vue';

export default {
  components: {
    RecommendationCard,
  },
  props: ['title', 'recommendations'],
};
</script>
