<template>
  <!-- eslint-disable max-len -->
  <div class="flex w-full mx-auto cursor-pointer md:hover:bg-gray-300">
    <h1 class="text-gray-matcha py-6 md:py-4 md:py-2 text-xl md:text-base w-full md:w-auto text-center md:text-left">{{text}}</h1>
  </div>
</template>

<script>
export default {
  props: ['text'],
};
</script>
