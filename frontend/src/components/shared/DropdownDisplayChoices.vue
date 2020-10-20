<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none ml-2 sm:flex-none" @focusout="close" tabindex="0">
    <div v-bind:class="{'settings-button-choice': true, 'rounded-lg': true , 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">
        {{ getName }}<span class="ml-2">▼</span></h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'z-10': true, 'h-auto': options.length < 5 , 'hidden': closed, 'right-0': position === 'right', 'md:right-auto': position === 'right'}">
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
  props: ['options', 'name', 'position', 'startingOptions', 'min', 'max'],
  data: () => ({
    closed: true,
    selectedFilters: [],
  }),
  methods: {
    select(option) {
      const optionIndex = this.selectedFilters.indexOf(option);
      if (optionIndex !== -1) {
        if (this.selectedFilters.length > this.min) {
          this.selectedFilters.splice(optionIndex, 1);
          this.$emit('save-multiple-choice', this.name, this.selectedFilters);
        }
      } else if (this.selectedFilters.length < this.max) {
        this.selectedFilters.push(option);
        this.$emit('save-multiple-choice', this.name, this.selectedFilters);
      }
    },
    toggle() {
      this.closed = !this.closed;
    },
    close() {
      this.closed = true;
    },
  },
  computed: {
    getName() {
      if (this.selectedFilters.length) {
        return this.selectedFilters[0];
      }
      return this.name;
    },
  },
  beforeMount() {
    if (this.startingOptions) {
      this.selectedFilters = this.startingOptions;
    }
  },
};
</script>
