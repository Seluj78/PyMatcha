<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none flex-1 sm:flex-none" @focusout="close" tabindex="0">
    <div v-bind:class="{'sort-button': true, 'border-gray-matcha': !closed}" @click="toggle">
<!--      <img v-bind:class="{ 'opacity-50': closed, 'noSelect': true }" src="../../assets/sort.png">-->
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">↑↓</h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'hidden': closed}">
        <h1 v-for="(option, index) in options" :key="option + index + option"
          v-bind:class="{'sort-dropdown-option': true, 'border-b': index !== options.length - 1}"
          v-on:click="select(option)">
          {{option}}
        </h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['options', 'name'],
  data: () => ({
    closed: true,
  }),
  methods: {
    select(option) {
      this.closed = true;
      this.$emit('sort', option);
    },
    toggle() {
      this.closed = !this.closed;
    },
    close() {
      this.closed = true;
    },
  },
};
</script>
