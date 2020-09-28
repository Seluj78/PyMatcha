<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none ml-2 flex-1 sm:flex-none" @focusout="close" tabindex="0">
    <div v-bind:class="{'filter-button': true, 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">{{name}}</h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'hidden': closed, 'right-0': position === 'right', 'md:right-auto': position === 'right'}">
      <h1 v-for="(option, index) in options" :key="option + index + option"
          v-bind:class="{'sort-dropdown-option': true, 'border-b': index !== options.length - 1, 'capitalize': true}"
          v-on:click="select(option)">
        {{option}}
      </h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['options', 'name', 'position'],
  data: () => ({
    closed: true,
    selectedFilters: [],
  }),
  methods: {
    select(option) {
      this.selectedFilters.push(option);
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
