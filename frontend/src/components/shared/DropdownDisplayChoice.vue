<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none sm:flex-none" @focusout="close" tabindex="0">
    <div v-bind:class="{'settings-button-choice': true, 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">{{ currentOption }}<span class="ml-2">▼</span></h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'z-10': true , 'hidden': closed, 'h-auto': options.length < 5}">
      <h1 v-for="(option, index) in options" :key="option + index + option"
          v-bind:class="{'capitalize': true, 'sort-dropdown-option': true, 'border-b': index !== options.length - 1, 'font-extrabold': option === currentOption, 'text-gray-matcha': option === currentOption}"
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
      this.close();
      this.currentOption = option;
      this.$emit('save-single-choice', this.name, option);
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
