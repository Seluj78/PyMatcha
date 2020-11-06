<template>
  <!-- eslint-disable max-len -->
    <div class="mb-8" ref="sliderDropdown">
      <div class="mx-auto flex w-full items-center mb-4 max-w-md">
        <div class="w-full flex justify-between">
          <h1 class="text-base text-purple-matcha capitalize">{{ name }}</h1>
          <h1 class="text-base text-purple-matcha">
            <span class="">{{this.slider.startMin}}<span v-if="oneHandle"> {{this.unit}}</span></span>
            <span v-if="!oneHandle"> to </span>
            <span v-if="!oneHandle" class="">{{this.slider.startMax}} {{this.unit}}</span></h1>
        </div>
      </div>
      <div ref="slider" class="mx-auto w-full mb-4 px-4 max-w-md"></div>
    </div>
</template>

<script>
import noUiSlider from 'nouislider';
import 'nouislider/distribute/nouislider.css';

export default {
  props: ['options', 'name', 'unit', 'min', 'max', 'oneHandle'],
  data: () => ({
    slider: {
      startMin: null,
      startMax: null,
      min: null,
      max: null,
      start: null,
      step: 1,
    },
  }),
  mounted() {
    this.slider.startMin = this.min;
    this.slider.startMax = this.max;
    this.slider.min = this.min;
    this.slider.max = this.max;
    this.slider.start = this.min;
    let start;
    if (this.oneHandle) {
      start = 0;
    } else {
      start = [this.slider.startMin, this.slider.startMax];
    }
    noUiSlider.create(this.$refs.slider, {
      start,
      step: this.slider.step,
      range: {
        min: this.slider.min,
        max: this.slider.max,
      },
    });
    this.$refs.slider.noUiSlider.on('update', (values) => {
      this.slider.startMin = parseInt(values[0], 10);
      this.slider.startMax = parseInt(values[1], 10);
      this.$emit('save-filter', this.name, this.slider.startMin, this.slider.startMax, this.oneHandle);
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
