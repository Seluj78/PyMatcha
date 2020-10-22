<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none sm:flex-none cursor-pointer" @focusout="close" tabindex="0">
    <div v-bind:class="{'onboarding-sub-container-content-heading': true, 'border': true, 'px-4': true, 'py-2': true, 'rounded-md': true, 'text-center': true, 'text-2xl': true, 'sm:text-5xl': true, 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-100': closed, 'noSelect': true, 'capitalize': true }">{{ currentOption }}<span v-if="closed" class="ml-2">▼</span><span v-if="!closed" class="ml-2">▲</span></h1>
    </div>
    <div v-bind:class="{'sort-dropdown': true, 'max-w-xs': true, 'mx-auto': true, 'left-0': position === 'left' || position === 'center', 'right-0': position === 'right' || position === 'center', 'z-10': true, 'hidden': closed, 'h-auto': options.length < 5}">
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
      console.log(option);
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
  deactivated() {
    if (!this.$route.path.startsWith('/users')) {
      this.currentOption = this.startingOption;
    }
  },
};
</script>
