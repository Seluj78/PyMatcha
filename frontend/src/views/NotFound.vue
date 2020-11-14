<template>
  <!-- eslint-disable max-len -->
  <div class="sm:mx-16 lg:mx-32 mt-32">
    <div class="flex flex-col">
      <div class="mx-auto flex flex-row items-center justify-center">
        <h1 class="text-2xl sm:text-4xl text-center text-gray-matcha leading-none opacity-50">404</h1>
        <img src="../assets/brokenHeartBlue.png" class="ml-2 h-6 sm:h-8 opacity-50">
      </div>
      <h1 class="text-center text-6xl sm:text-8xl text-gray-matcha my-8 leading-none">Page not found</h1>
    </div>
    <h1 @click="$router.go(-1)" class="onboarding-sub-container-content-button-outline-light mx-auto">Back</h1>
  </div>
</template>
