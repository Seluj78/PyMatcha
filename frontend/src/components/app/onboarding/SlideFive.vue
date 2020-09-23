<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1>{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">Bio</h1>
    <p class="mt-2">{{textareaLength}} / {{maxTextareaLength}}</p>
    <div class="h-64 flex flex-col items-center justify-center w-full">
      <textarea v-model="textareaValue" style="resize: none;" class="focus:outline-none active:outline-none w-full h-full border border-gray-matcha py-2 px-4 my-8 rounded-md text-gray-matcha" placeholder="I am best described as ..."></textarea>
    </div>
    <button class="onboarding-sub-container-content-button-outline-light mt-0" v-on:click="saveInput()">{{slide.buttonText}}</button>
  </section>
</template>

<script>
import Vue from 'vue';

export default {
  props: ['slide'],
  data: () => ({
    optionSelected: null,
    maxTextareaLength: 200,
    textareaValue: '',
    bus: new Vue(),
  }),
  methods: {
    saveInput() {
      this.$emit('saveInput', 'slideOne', this.optionSelected, 0);
    },
    select(...args) {
      const [val] = args;
      this.optionSelected = val;
      this.bus.$emit('deselectIfNot', val);
    },
  },
  computed: {
    textareaLength() {
      return this.textareaValue.length;
    },
  },
};
</script>
