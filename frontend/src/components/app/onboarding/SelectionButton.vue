<template>
  <h1
    v-bind:class="{
        'onboarding-sub-container-content-button-outline': true,
        'mt-2': true,
        'capitalize': true,
        'onboarding-sub-container-content-button-outline-selected': selected,
        'cursor-default': invalid,
      }"
    v-on:click="select(val)">
    {{val}}
  </h1>
</template>

<script>
/* eslint-disable max-len */

export default {
  props: ['val', 'canBeSelected', 'bus'],
  data: () => ({
    selected: false,
  }),
  methods: {
    select(val) {
      if (this.invalid) {
        return;
      }
      if (this.selected) {
        this.selected = false;
        this.$emit('deselect', val);
      } else {
        this.selected = true;
        this.$emit('select', val);
      }
    },
    deselectIfNot(selectedVal) {
      if (this.val !== selectedVal) {
        this.selected = false;
      }
    },
  },
  computed: {
    invalid() {
      return !this.selected && !this.canBeSelected;
    },
  },
  mounted() {
    this.bus.$on('deselect-if-not', this.deselectIfNot);
  },
};
</script>
