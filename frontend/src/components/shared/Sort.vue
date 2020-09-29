<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none flex-1 sm:flex-none" @focusout="close" tabindex="0">
    <div v-bind:class="{'sort-button': true, 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">↑↓</h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'hidden': closed, 'left-0': position === 'left', 'md:left-auto': position === 'left'}">
        <h1 v-for="(option, index) in options" :key="option + index + option"
          v-bind:class="{'sort-dropdown-option': true, 'border-b': index !== options.length - 1, 'font-extrabold': option === currentOption, 'text-gray-matcha': option === currentOption}"
          v-on:click="select(option)">
          {{option}}
        </h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['options', 'name', 'position', 'startingOption'],
  data: () => ({
    closed: true,
    currentOption: '',
  }),
  methods: {
    select(option) {
      this.closed = true;
      this.currentOption = option;
      this.$emit('saveSort', option);
    },
    toggle() {
      this.closed = !this.closed;
    },
    close() {
      this.closed = true;
    },
  },
  beforeMount() {
    this.currentOption = this.startingOption;
  },
};
</script>
