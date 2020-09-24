<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1 class="text-gray-matcha">{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">{{slide.header}}</h1>
    <div v-bind:class="{'onboarding-selection-button-container': true, 'justify-center': slide.options.length < 5}">
      <SelectionButton v-for="(option, index) in slide.options" :key="index + option"
        v-bind:val="option"
        v-bind:canBeSelected="true"
        v-bind:bus="bus"
        v-on:select="select"
        v-on:deselect="deselect">
      </SelectionButton>
    </div>
    <button
      v-bind:disabled="!optionSelected"
      v-bind:class="{
        'onboarding-sub-container-slide-button': true,
        'opacity-25': !optionSelected,
        'cursor-default': !optionSelected}"
      v-on:click="saveInput()">
      {{slide.buttonText}}
    </button>
  </section>
</template>

<script>
import Vue from 'vue';
import SelectionButton from '@/components/app/onboarding/SelectionButton.vue';

export default {
  components: {
    SelectionButton,
  },
  props: ['slide'],
  data: () => ({
    optionSelected: null,
    bus: new Vue(),
  }),
  methods: {
    saveInput() {
      this.$emit('saveInput', this.slide.key, this.optionSelected);
      this.optionSelected = null;
    },
    select(...args) {
      const [val] = args;
      this.optionSelected = val;
      this.bus.$emit('deselectIfNot', val);
    },
    deselect() {
      this.optionSelected = '';
    },
  },
};
</script>
