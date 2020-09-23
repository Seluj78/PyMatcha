<template>
  <h1
    v-bind:class="{
        'onboarding-sub-container-content-button-outline': true,
        'mt-2': true,
        'onboarding-sub-container-content-button-outline-selected': selected,
      }"
    v-on:click="select(val)">{{val}}</h1>
</template>

<script>
export default {
  props: ['val', 'bus'],
  data: () => ({
    selected: false,
    selectedValue: '',
  }),
  methods: {
    select(val) {
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
  mounted() {
    this.bus.$on('deselectIfNot', this.deselectIfNot);
  },
};
</script>
