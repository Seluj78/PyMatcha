<template>
  <!-- eslint-disable max-len -->
  <section class="onboarding-sub-container">
    <h1 class="text-gray-matcha">{{slide.current}} / {{slide.count}}</h1>
    <h1 class="onboarding-sub-container-content-heading leading-none">Bio</h1>
    <p class="mt-2 text-gray-matcha">{{textareaLength}} / {{slide.maxTextareaLength}}</p>
    <div class="h-64 flex flex-col items-center justify-center w-full">
      <textarea
        autofocus
        v-bind:maxlength="slide.maxTextareaLength"
        v-model="textareaValue"
        style="resize: none;"
        class="onboarding-textarea"
        v-bind:placeholder="slide.placeholder">
      </textarea>
    </div>
    <button
      v-bind:disabled="textareaValue.length < slide.minTextareaLength"
      v-bind:class="{
        'onboarding-sub-container-slide-button': true,
        'opacity-25': textareaValue.length < slide.minTextareaLength,
        'cursor-default': textareaValue.length < slide.minTextareaLength}"
      v-on:click="saveInput()">
      {{slide.buttonText}}
    </button>
  </section>
</template>

<script>

export default {
  props: ['slide'],
  data: () => ({
    textareaValue: '',
  }),
  methods: {
    saveInput() {
      this.$emit('saveInput', this.slide.key, this.textareaValue);
    },
  },
  computed: {
    textareaLength() {
      return this.textareaValue.length;
    },
  },
};
</script>
