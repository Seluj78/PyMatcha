<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none ml-2 flex-1 sm:flex-none" @focusout="close" tabindex="0">
    <div v-bind:class="{'filter-button': true, 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">
        {{name}}</h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'h-auto': options.length < 5 , 'hidden': closed, 'right-0': position === 'right', 'md:right-auto': position === 'right'}">
      <h1 v-for="(option, index) in options" :key="option + index + option"
          v-bind:class="{'sort-dropdown-option': true, 'border-b': index !== options.length - 1, 'capitalize': true,
          'font-extrabold': selectedFilters.indexOf(option) !== -1, 'text-gray-matcha': selectedFilters.indexOf(option) !== -1}"
          v-on:click="select(option)">
        {{option}}
      </h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['options', 'name', 'position', 'startingOptions'],
  data: () => ({
    closed: true,
    selectedFilters: [],
  }),
  methods: {
    select(option) {
      const optionIndex = this.selectedFilters.indexOf(option);
      if (optionIndex !== -1) {
        this.selectedFilters.splice(optionIndex, 1);
        this.$emit('saveFilterMultiple', this.name, this.selectedFilters);
      } else {
        this.selectedFilters.push(option);
        this.$emit('saveFilterMultiple', this.name, this.selectedFilters);
      }
    },
    toggle() {
      this.closed = !this.closed;
    },
    close() {
      this.closed = true;
    },
  },
  beforeMount() {
    if (this.startingOptions) {
      this.selectedFilters = this.startingOptions;
    }
  },
};
</script>
