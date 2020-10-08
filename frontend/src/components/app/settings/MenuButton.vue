<template>
  <!-- eslint-disable max-len -->
  <div class="flex w-full mx-auto cursor-pointer hover:bg-gray-300">
    <h1 class="text-gray-matcha py-4 text-xl w-full md:w-auto text-center md:text-left text-lg">{{text}}</h1>
  </div>
</template>

<script>
export default {
  props: ['text'],
};
</script>
