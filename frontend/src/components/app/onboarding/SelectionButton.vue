<template>
  <h1
    v-bind:class="{
        'onboarding-sub-container-content-button-outline': true,
        'mt-2': true,
        'onboarding-sub-container-content-button-outline-selected': selected,
        'cursor-default': invalid,
      }"
    v-on:click="select(val)">{{val}}</h1>
</template>

<script>
/* eslint-disable max-len */

export default {
  props: ['val', 'bus'],
  data: () => ({
    selected: false,
    selectedValue: '',
  }),
  methods: {
    select(val) {
      if (!this.selected && this.$parent.maxInterests && this.$parent.optionSelected.length === this.$parent.maxInterests) {
        return;
      }
      if (this.selected) {
        this.selected = false;
        this.selectedValue = '';
        this.$emit('deselect', val);
        return;
      }
      this.selected = true;
      this.selectedValue = val;
      this.$emit('select', val);
    },
    deselectIfNot(selectedVal) {
      if (this.val !== selectedVal) {
        this.selected = false;
      }
    },
  },
  computed: {
    invalid() {
      return !this.selected && this.$parent.maxInterests && this.$parent.optionSelected.length === this.$parent.maxInterests;
    },
  },
  mounted() {
    this.bus.$on('deselectIfNot', this.deselectIfNot);
  },
};
</script>
