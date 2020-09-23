<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1>{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">Orientation</h1>
    <div class="h-64 flex flex-col items-center justify-center w-full">
      <SelectionButton v-bind:val="'Heterosexual'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'Homosexual'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'Bi-sexual'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
      <SelectionButton v-bind:val="'Other'" v-bind:bus="bus" v-on:select="select" v-on:deselect="deselect"></SelectionButton>
    </div>
    <button v-bind:disabled="!optionSelected" v-bind:class="{'onboarding-sub-container-content-button-outline-light': true, 'mt-0': true, 'opacity-25': !optionSelected, 'cursor-default': !optionSelected}" v-on:click="saveInput()">{{slide.buttonText}}</button>
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
      this.$emit('saveInput', 'slideTwo', this.optionSelected, 0);
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
