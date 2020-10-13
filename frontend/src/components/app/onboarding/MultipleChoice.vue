<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1 class="text-gray-matcha">{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">{{slide.header}}</h1>
    <p class="mt-2 text-gray-matcha">{{optionsSelectedCount}} / {{slide.maxOptionsForSelection}}</p>
    <div v-bind:class="{'onboarding-selection-button-container': true, 'justify-center': slide.options.length < 5}">
      <SelectionButton v-for="(option, index) in slide.options" :key="index + option"
        v-bind:val="option"
        v-bind:canBeSelected="canSelectMoreOptions"
        v-bind:bus="bus"
        v-on:select="select"
        v-on:deselect="deselect">
      </SelectionButton>
    </div>
    <button
      v-bind:disabled="!minimumSelectionsMade"
      v-bind:class="{
        'onboarding-sub-container-slide-button': true,
        'opacity-25': !minimumSelectionsMade,
        'cursor-default': !minimumSelectionsMade}"
      v-on:click="saveInput()">
      {{slide.buttonText}}
    </button>
  </section>
</template>

<script>
/* eslint-disable  vue/custom-event-name-casing */
import Vue from 'vue';
import SelectionButton from '@/components/app/onboarding/SelectionButton.vue';

export default {
  components: {
    SelectionButton,
  },
  props: ['slide'],
  data: () => ({
    optionSelected: [],
    bus: new Vue(),
  }),
  methods: {
    saveInput() {
      this.$emit('saveInput', this.slide.key, this.optionSelected);
      this.optionSelected = [];
    },
    select(...args) {
      if (this.canSelectMoreOptions) {
        const [val] = args;
        this.optionSelected.push(val);
      }
    },
    deselect(val) {
      this.optionSelected = this.optionSelected.filter((option) => option !== val);
    },
  },
  computed: {
    optionsSelectedCount() {
      return this.optionSelected.length;
    },
    canSelectMoreOptions() {
      return this.optionsSelectedCount < this.slide.maxOptionsForSelection;
    },
    minimumSelectionsMade() {
      return this.optionSelected.length >= this.slide.minOptionsForSelection;
    },
  },
};
</script>
