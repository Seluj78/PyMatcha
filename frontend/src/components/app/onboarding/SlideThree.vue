<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1>{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">I like</h1>
    <div class="h-64 pb-4 my-8 border-b-2 max-w-xs border-purple-matcha flex flex-col items-center w-full overflow-scroll">
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'coffee'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
    </div>
    <button v-bind:disabled="!optionSelected.length" v-bind:class="{'onboarding-sub-container-content-button-outline-light': true, 'mt-0': true, 'opacity-25': !optionSelected.length, 'cursor-default': !optionSelected.length}" v-on:click="saveInput()">{{slide.buttonText}}</button>
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
    optionSelected: [],
    bus: new Vue(),
  }),
  methods: {
    saveInput() {
      this.$emit('saveInput', 'slideThree', this.optionSelected, 0);
    },
    select(...args) {
      const [val] = args;
      this.optionSelected.push(val);
    },
    deselect(val) {
      this.optionSelected = this.optionSelected.filter((e) => e !== val);
    },
  },
};
</script>
