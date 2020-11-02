<template>
  <!-- eslint-disable max-len -->
  <div class="ml-auto mr-8 cursor-pointer relative pr-1">
    <img src="../../assets/bell.png" class="w-5">
    <div v-if="notify" class="w-3 h-3 bg-purple-matcha rounded-full absolute right-0 bottom-0 ml-2 pl-1"></div>
  </div>
</template>

<script>
export default {
  data: () => ({
    notify: false,
  }),
};
</script>
