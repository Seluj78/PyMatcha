<template>
  <!-- eslint-disable max-len -->
  <div class='mx-auto max-w-md mb-4'>
    <h1 class="text-xl lg text-purple-matcha capitalize text-left">{{ name }}</h1>
    <h1 class="text-md text-left opacity-50 mb-4">{{ info }}</h1>
    <div class="h-48 w-auto overflow-scroll rounded-md border border-gray-300 bg-white">
      <h1 v-for="(option, index) in options" :key="option + index + option"
          v-bind:class="{'sort-dropdown-option': true, 'text-base': true, 'border-b': index !== options.length - 1, 'capitalize': true,
          'font-extrabold': selectedFilters.indexOf(option) !== -1, 'text-gray-matcha': selectedFilters.indexOf(option) !== -1}"
          v-on:click="select(option)">
        {{option}}
      </h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['options', 'name', 'info', 'position'],
  data: () => ({
    closed: true,
    selectedFilters: [],
  }),
  methods: {
    select(option) {
      const optionIndex = this.selectedFilters.indexOf(option);
      if (optionIndex !== -1) {
        this.selectedFilters.splice(optionIndex, 1);
        this.$emit('save-filter-multiple', this.name, this.selectedFilters);
      } else {
        this.selectedFilters.push(option);
        this.$emit('save-filter-multiple', this.name, this.selectedFilters);
      }
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
