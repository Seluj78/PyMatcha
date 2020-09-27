<template>
  <!-- eslint-disable max-len -->
  <div class="inline-block focus:outline-none">
    <div v-bind:class="{'flex': true, 'items-center': true, 'justify-center': true, 'w-20': true, 'h-12': true, 'rounded-xl': true, 'border': true, 'border-gray-matcha': !closed, 'border-gray-300': closed, 'px-4': true, 'py-2': true, 'focus:outline-none': true, 'cursor-pointer': true}" @click="toggle" @focusout="close" tabindex="0">
      <img v-bind:class="{ 'opacity-50': closed, 'h-8': true, }" src="../../assets/sort.png">
    </div>
    <div v-bind:class="{
      'w-56': true,
      'h-56': true,
      'mt-4': true,
      'overflow-scroll': true,
      'rounded-md': true,
      'shadow-2xl': true,
      'absolute': true,
      'rounded-md': true,
      'bg-white': true,
      'hidden': closed}">
        <h1
          v-for="(option, index) in options"
          :key="option + index + option"
          v-bind:class="{
            'cursor-pointer': true,
            'block': true,
            'pl-4': true,
            'border-b': index !== options.length - 1,
            'border-gray-300': index !== options.length - 1,
            'py-4': true,
            'text-sm': true,
            'leading-5': true,
            'text-gray-700': true,
            'hover:bg-gray-100': true,
            'hover:text-gray-900': true,
            'focus:outline-none': true,
            'focus:bg-gray-100': true,
            'focus:text-gray-900': true}"
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
      this.$emit('sort', this.name, option);
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
