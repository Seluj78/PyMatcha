<template>
  <!-- eslint-disable max-len -->
  <div class="home mx-4">
    <section class="shadow-lg mb-8 h-full flex rounded-lg">
      <div class="intro bg-white-matcha rounded-lg w-full md:w-2/3
  flex flex-col justify-center md:rounded-tr-none md:rounded-br-none">
        <div class="mx-auto text-center md:text-left py-8 lg:py-0">
          <h1 class="text-5xl sm:text-6xl font-bold text-gray-matcha">Someone<br>
            is waiting<br>
            for you</h1>
          <h1 class="text-2xl text-gray-matcha pb-10 pt-6">Matcha is a free dating<br>
            app to find you a lover</h1>
          <router-link class="button-purple z-10" to="/accounts/signup">Get started</router-link>
        </div>
      </div>
      <div class="image hidden md:inline-block overflow-hidden md:w-1/3">
        <img src="../assets/home/couple.jpeg" class="w-full h-full object-cover rounded-tr-lg rounded-br-lg">
      </div>
    </section>
    <div class="pitch shadow-lg rounded-lg py-16 px-8 mb-8 w-full flex flex-col justify-center lg:px-16">
      <h1 class="text-4xl md:text-6xl text-white-matcha text-center font-bold leading-none">Set up dates effortlessly</h1>
      <h1 class="text-2xl pt-8 text-white-matcha text-center">No more awkward approaches</h1>
      <h1 class="text-2xl pt-4 text-white-matcha text-center">No more lonely Friday nights</h1>
    </div>
    <div class="bg-white-matcha py-16 mb-8">
      <h1 class="text-4xl md:text-6xl text-center font-bold leading-none text-gray-matcha mb-16">How it works</h1>
      <cardImg v-bind:cardSrc="likeSomeoneCard"></cardImg>
      <imgCard class="mt-24" v-bind:cardSrc="getMatchedCard"></imgCard>
      <cardImg class="mt-24" v-bind:cardSrc="chatCard"></cardImg>
    </div>
    <div class="w-full mb-8 rounded-lg shadow-lg">
      <div class="relative rounded-lg" style="padding-bottom: 70%">
        <img src="../assets/home/couple2.jpg" class="absolute object-cover h-full w-full rounded-lg">
        <h1 class="text-gray-matcha text-center text-2xl sm:text-5xl lg:text-6xl font-bold absolute bottom-0 w-full p-8"><span class="bg-white-matcha">"I met Travis via Matcha, and he
          is the coolest dude fo sure" - Kylie</span></h1>
      </div>
    </div>
    <div class="bg-white-matcha overflow-hidden relative shadow-lg rounded-lg py-32 px-8 w-full flex flex-col justify-center lg:px-16">
      <h1 class="text-4xl md:text-6xl text-gray-matcha text-center font-bold leading-none z-10">It is your turn</h1>
      <h1 class="text-2xl text-gray-matcha text-center my-8 z-10">More than 4 million people matched</h1>
      <router-link class="button-purple z-10" to="/accounts/signup">Get started</router-link>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>

import Footer from '@/components/shared/Footer.vue';
import imgCard from '@/components/home/imgCard.vue';
import cardImg from '@/components/home/cardImg.vue';
import likeSomeone from '@/assets/home/likeSomeone.png';
import match from '@/assets/home/match.png';
import chat from '@/assets/home/chat.png';

export default {
  name: 'Home',
  components: {
    Footer,
    imgCard,
    cardImg,
  },
  data: () => ({
    likeSomeoneCard: {
      imgSrc: likeSomeone,
      cardTitle: 'Like',
      cardDescription: [
        'Based on age, location,',
        'popularity and interests.',
      ],
    },
    getMatchedCard: {
      imgSrc: match,
      cardTitle: 'Match',
      cardDescription: [
        'If person you liked likes you,',
        'you have a match.',
      ],
    },
    chatCard: {
      imgSrc: chat,
      cardTitle: 'Meet',
      cardDescription: [
        'Chat with matches',
        'and set up dates.',
      ],
    },
  }),
};
</script>

<style scoped>
.home {
  height: calc(100% - 4rem - 2rem);
}

.pitch {
  background-color: #ad1deb;
  background-image: linear-gradient(315deg, #ad1deb 0%, #6e72fc 74%);
}
</style>
