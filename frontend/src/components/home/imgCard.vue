<template>
  <!-- eslint-disable max-len -->
  <section class="md:flex md:items-center">
    <div id="card" class="md:w-1/2 md:order-2 my-10 md:my-0 text-center md:text-left">
      <div class="w-10/12 md:w-8/12 mx-auto">
        <h1 class="text-4xl md:text-6xl font-bold pb-2 leading-none howItWorksHeader">{{cardSrc.cardTitle}}</h1>
        <h2 v-for="description in cardSrc.cardDescription"
            v-bind:key="description" class="text-2xl text-gray-matcha">{{description}}</h2>
      </div>
    </div>
    <div id="img" class="md:w-1/2 md:order-1">
      <img v-bind:src="cardSrc.imgSrc" class="w-8/12 mx-auto">
    </div>
  </section>
</template>

<script>
/* eslint-disable indent */
/* eslint-disable quotes */

export default {
  name: 'imgCard',
  props: ['cardSrc'],
};
</script>

<style scoped>
.howItWorksHeader {
  background: linear-gradient(315deg, #6e72fc 30%, #ad1deb 74%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
