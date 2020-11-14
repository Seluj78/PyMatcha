<template>
  <!-- eslint-disable max-len -->
  <div class="flex w-full mx-auto cursor-pointer md:hover:bg-purple-matcha-menu-hover">
    <h1 class="text-gray-matcha py-6 md:py-4 md:py-2 text-xl md:text-base w-full md:w-auto text-center mx-auto">{{text}}</h1>
  </div>
</template>

<script>
export default {
  props: ['text'],
};
</script>
