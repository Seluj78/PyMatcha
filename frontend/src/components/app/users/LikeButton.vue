<template>
  <!-- eslint-disable max-len -->
  <div class="w-full">
    <div @mouseover="hover = true"
         @mouseleave="hover = false"
         @click="toggle()"
         class="w-full flex justify-center items-center bg-purple-matcha py-4 rounded-lg cursor-pointer">
      <img v-bind:src="getImage" class="h-8">
      <h1 class="text-white-matcha text-2xl ml-2 font-bold">{{getText}}</h1>
    </div>
    <h1 v-if="description && !hasBeenClicked" class="text-purple-matcha text-sm mt-2"><span v-if="counter" class="font-bold">{{counter}}. </span>{{description}}</h1>
  </div>
</template>

<script>
/* eslint-disable max-len */

export default {
  props: [
    'name',
    'startImage',
    'hoverImage',
    'clickedImage',
    'text',
    'textRevert',
    'counter',
    'description',
    'hasBeenClicked',
  ],
  data: () => ({
    hover: false,
    clicked: false,
  }),
  methods: {
    toggle() {
      this.clicked = !this.clicked;
      if (this.clicked) {
        this.$emit('clicked', this.name);
      } else {
        this.$emit('revert', this.name);
      }
    },
  },
  computed: {
    getImage() {
      if (this.clicked) {
        return this.clickedImage;
      }
      if (this.hover) {
        return this.hoverImage;
      }
      return this.startImage;
    },
    getText() {
      if (this.clicked) {
        return this.textRevert;
      }
      return this.text;
    },
  },
  beforeMount() {
    if (this.hasBeenClicked) {
      this.clicked = true;
    }
  },
};
</script>
