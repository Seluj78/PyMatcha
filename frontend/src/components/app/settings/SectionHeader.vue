<template>
  <div class="flex max-w-sm justify-between items-center w-full my-4">
    <h1 class="text-3xl text-purple-matcha capitalize">{{ name }}</h1>
    <div class="md:hidden sort-button rounded-md text-lg w-12">
      <h1 class="noSelect">←</h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['name'],
};
</script>
