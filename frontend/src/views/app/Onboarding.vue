<template>
  <!-- eslint-disable max-len -->
  <div class="onboarding-container">
    <section class="onboarding-sub-container" v-if="slide === 0">
      <h1 class="onboarding-sub-container-content-heading text-8xl introduction mb-8 text-center leading-none">Meet<br>your<br>lover</h1>
      <button class="onboarding-sub-container-content-button-outline w-1/2 mt-0" v-on:click="nextSlide()">{{buttonText}}</button>
    </section>
    <section class="onboarding-sub-container" v-if="slide === 1">
      <h1>{{slide}} / {{slideCount}}</h1>
      <h1 class="onboarding-sub-container-content-heading leading-none">I am</h1>
      <div class="h-64 flex flex-col items-center justify-center w-full">
        <h1 class="onboarding-sub-container-content-button-outline mt-0">Man</h1>
        <h1 class="onboarding-sub-container-content-button-outline mt-2">Woman</h1>
        <h1 class="onboarding-sub-container-content-button-outline mt-2">Other</h1>
      </div>
      <button class="onboarding-sub-container-content-button-outline-light mt-0" v-on:click="nextSlide()">{{buttonText}}</button>
    </section>
    <section class="onboarding-sub-container" v-if="slide === 2">
      <h1>{{slide}} / {{slideCount}}</h1>
      <h1 class="onboarding-sub-container-content-heading leading-none">I want</h1>
      <div class="h-64 flex flex-col items-center justify-center w-full">
        <h1 class="onboarding-sub-container-content-button-outline mt-0">Men</h1>
        <h1 class="onboarding-sub-container-content-button-outline mt-2">Women</h1>
        <h1 class="onboarding-sub-container-content-button-outline mt-2">Other</h1>
      </div>
      <button class="onboarding-sub-container-content-button-outline-light mt-0" v-on:click="nextSlide()">{{buttonText}}</button>
    </section>
    <section class="onboarding-sub-container" v-if="slide === 3">
      <h1>{{slide}} / {{slideCount}}</h1>
      <h1 class="onboarding-sub-container-content-heading leading-none">I like</h1>
      <div class="h-64 pb-4 my-8 sm:my-16 flex flex-col items-center w-full overflow-scroll">
        <h1 class="onboarding-sub-container-content-button-outline mt-0">coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">yoga</h1>
        <h1 class="onboarding-sub-container-content-button-outline">football</h1>
        <h1 class="onboarding-sub-container-content-button-outline">rap</h1>
        <h1 class="onboarding-sub-container-content-button-outline">travelling</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
        <h1 class="onboarding-sub-container-content-button-outline">Coffee</h1>
      </div>
      <button class="onboarding-sub-container-content-button-outline-light mt-0" v-on:click="nextSlide()">{{buttonText}}</button>
    </section>
    <section class="onboarding-sub-container" v-if="slide === 4">
      <h1>{{slide}} / {{slideCount}}</h1>
      <h1 class="onboarding-sub-container-content-heading leading-none text-center">Profile<br>image</h1>
        <button v-if="!slide4.imageUploaded" class="relative onboarding-sub-container-upload-button my-8">
          <input class="cursor-pointer opacity-0 absolute top-0 left-0 w-full h-full rounded-md" type="file" v-on:change="selectFile()" ref="file">ADD
        </button>

      <div class="w-full relative" v-if="slide4.imageUploaded">
        <img src="../../assets/onboarding/remove.png" class="absolute cursor-pointer top-0 right-0 mt-6 -mr-3 w-8 z-10" v-on:click="deleteImage()">
        <div class="relative overflow-hidden bg-red-600 rounded-lg w-full my-10" style="padding-bottom: 70%">
          <img v-bind:src="slide4.imageUrl" class="absolute object-cover w-full h-full rounded-lg">
        </div>
      </div>
      <button class="onboarding-sub-container-content-button-outline-light mt-0" v-on:click="nextSlide()">{{buttonText}}</button>
    </section>
    <section class="onboarding-sub-container" v-if="slide === 5">
      <h1>{{slide}} / {{slideCount}}</h1>
      <h1 class="onboarding-sub-container-content-heading leading-none text-center">Other<br>images</h1>
      <button class="onboarding-sub-container-upload-button my-8" v-on:click="nextSlide()">ADD</button>
      <div class="uploaded-image-container">
      </div>
      <button class="onboarding-sub-container-content-button-outline-light mt-0" v-on:click="nextSlide()">{{buttonText}}</button>
    </section>
  </div>
</template>

<script>

export default {
  data: () => ({
    slide: 0,
    slideCount: 6,
    slide4: {
      image: null,
      imageUrl: null,
      imageUploaded: false,
      imageUploadError: false,
      errorText: '',
    },
  }),
  methods: {
    nextSlide() {
      if (this.slide === this.slideCount) {
        this.$router.push('/browse');
      }
      if (this.slide < this.slideCount) {
        this.slide += 1;
      }
    },
    selectFile() {
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      const file = this.$refs.file.files[0];
      this.slide4.file = file;

      if (!allowedTypes.includes(file.type)) {
        this.slide4.errorText = 'Only images allowed';
        this.slide4.imageUploadError = true;
        return;
      }
      if (file.size > 2000000) {
        this.slide4.errorText = 'File too large';
        this.slide4.imageUploadError = true;
        return;
      }
      this.slide4.imageUploaded = true;
      this.slide4.imageUrl = URL.createObjectURL(file);
      console.log(this.slide4.imageUrl);
    },
    deleteImage() {
      this.slide4.image = null;
      this.slide4.imageUploaded = false;
      this.slide4.imageUrl = '';
    },
  },
  computed: {
    buttonText() {
      if (this.slide === 0) {
        return 'Let\'s go';
      }
      if (this.slide < this.slideCount) {
        return 'Continue';
      }
      return 'Finish';
    },
  },
};

</script>

<style scoped>
.introduction {
  background: linear-gradient(315deg, #ad1deb 0%, #6e72fc 74%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.upload-small {
  height: 50%;
}
</style>
