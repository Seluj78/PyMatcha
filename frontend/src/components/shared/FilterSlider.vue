<template>
  <!-- eslint-disable max-len -->
  <div class="focus:outline-none ml-2 flex-1 sm:flex-none" @focusout="close" tabindex="1">
    <div v-bind:class="{'filter-button': true, 'border-gray-matcha': !closed}" @click="toggle">
      <h1 v-bind:class="{ 'opacity-50': closed, 'noSelect': true, 'capitalize': true }">{{name}}</h1>
    </div>
    <div ref="sliderDropdown" v-bind:class="{'slider-dropdown': true, 'hidden': closed}">
      <div class="flex mb-4 mt-2">
        <h1><span class="font-bold">{{this.slider.startMin}} {{this.unit}}</span> to <span class="font-bold">{{this.slider.startMax}} {{this.unit}}</span></h1>
      </div>
      <div ref="slider" class="w-64 mb-4"></div>
    </div>
  </div>
</template>

<script>
import noUiSlider from 'nouislider';
import 'nouislider/distribute/nouislider.css';

export default {
  props: ['options', 'name', 'unit'],
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
    select() {
      this.closed = true;
      const { min } = this.slider;
      const { max } = this.slider;
      this.$emit('filter', this.name, { min, max });
    },
    toggle() {
      this.closed = !this.closed;
      if (!this.closed) {
        this.$nextTick(function () {
          this.$refs.sliderDropdown.focus();
        });
      }
    },
    close(event) {
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
    this.$refs.slider.noUiSlider.on('update', (values) => {
      this.slider.startMin = parseInt(values[0], 10);
      this.slider.startMax = parseInt(values[1], 10);
    });
  },
};
</script>

<style>
.noUi-handle {
  outline: none;
}
.noUi-handle:focus {
  outline: none;
}
</style>
