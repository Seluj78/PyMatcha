<template>
  <!-- eslint-disable max-len -->
  <div class="inline-block focus:outline-none ml-2" @focusout="close" tabindex="1">
    <div v-bind:class="{'flex': true, 'items-center': true, 'justify-center': true, 'w-20': true, 'h-12': true, 'rounded-xl': true, 'border': true, 'border-gray-matcha': !closed, 'border border-gray-300': closed, 'px-12': true, 'py-2': true, 'focus:outline-none': true, 'cursor-pointer': true}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed }">{{name}}</h1>
    </div>
    <div id="sliderContainer" ref="afterClick" v-bind:class="{
      'h-16': true,
      'w-full': true,
      'max-w-xs': true,
      'mt-4': true,
      'flex': true,
      'items-center': true,
      'justify-center': true,
      'overflow-scroll': true,
      'rounded-md': true,
      'shadow-2xl': true,
      'absolute': true,
      'left-0': true,
      'rounded-md': true,
      'bg-white': true,
      'slider-bg': true,
      'hidden': closed}">
      <div ref="slider" class="focus:outline-none w-64"></div>
    </div>
  </div>
</template>

<script>
import noUiSlider from 'nouislider';
import 'nouislider/distribute/nouislider.css';

export default {
  props: ['options', 'name'],
  data: () => ({
    closed: true,
    slider: {
      startMin: 25,
      startMax: 75,
      min: 0,
      max: 100,
      start: 40,
      step: 1,
    },
  }),
  methods: {
    select(option) {
      this.closed = true;
      this.$emit('sort', this.name, option);
    },
    toggle() {
      this.closed = !this.closed;
      if (!this.closed) {
        this.$nextTick(function () {
          this.$refs.afterClick.focus();
        });
      }
    },
    close(event) {
      // console.log(event.currentTarget.id);
      if (!event.currentTarget.contains(event.relatedTarget)) {
        this.closed = true;
      }
    },
  },
  mounted() {
    noUiSlider.create(this.$refs.slider, {
      start: [this.slider.startMin, this.slider.startMax],
      step: this.slider.step,
      range: {
        min: this.slider.min,
        max: this.slider.max,
      },
    });
  },
};
</script>

<style>
.noUi-handle, .slider-bg {
  outline: none;
}
.noUi-handle:focus, .slider-bg:focus {
  outline: none;
}
</style>
