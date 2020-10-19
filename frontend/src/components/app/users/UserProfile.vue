<template>
  <!-- eslint-disable -->
  <div class="profileContainer">
    <div id="sliderScoreContainer" class="text-center w-full rounded-lt-md heatScore relative h-6">
      <div id="sliderScore" class="bg-purple-matcha absolute top-0 flex flex-col items-center justify-center h-12 w-auto rounded-b-md">
        <h1 class="text-white-matcha px-2"><span class="font-bold">{{user.heat_score}}</span> likes</h1>
      </div>
    </div>
    <div class="text-center text-wrap p-8 mt-4 border-b">
      <h1 class="text-gray-matcha text-4xl font-bold mb-6">{{user.first_name}}, {{user.age}}</h1>
      <div v-if="!user.is_online" class="flex items-center mt-2 text-left">
        <img class="w-3 h-3 mr-2" src="../../../assets/recommendations/offline.png">
        <h1 class="text-gray-600">Last seen {{user.last_seen}}</h1>
      </div>
      <div v-else class="flex items-center mt-2 text-left">
        <img class="w-3 h-3 mr-2" src="../../../assets/recommendations/online.png">
        <h1 class="text-gray-600">online</h1>
      </div>
      <div class="flex items-center mt-2 text-left">
        <img src="../../../assets/location.png" class="w-4 h-4 mr-2">
        <h1 class="text-gray-600">{{Math.floor(user.distance)}} km away</h1>
      </div>
      <div class="flex items-center mt-2 text-left">
        <img src="../../../assets/gender.png" class="w-4 h-4 mr-2">
        <h1 class="text-gray-600"><span class="capitalize">{{user.gender}}</span> looking for {{preferences()}}</h1>
      </div>
    </div>
    <div class="text-center text-wrap p-8 border-b">
      <h1>{{user.bio}}</h1>
      <div class="flex flex-wrap justify-center mx-auto mt-6">
        <h1 v-for="(interest, index) in userInterests" :key="index"
        class="px-4 py-1 border rounded-xl mr-2 mt-2 text-gray-600 text-sm">{{interest}}</h1>
      </div>
    </div>
    <div class="text-center flex flex-col mx-auto p-8 border-b">
      <div class="w-full flex justify-center items-center bg-purple-matcha py-4 rounded-lg cursor-pointer">
        <img src="../../../assets/heart.png" class="h-8">
        <h1 class="text-white-matcha text-2xl ml-2 font-bold">Like</h1>
      </div>
      <div class="w-full flex justify-center items-center bg-purple-matcha mt-8 py-4 rounded-lg cursor-pointer">
        <img src="../../../assets/superLike.png" class="h-8">
        <h1 class="text-white-matcha text-2xl ml-2 font-bold">Super Like</h1>
      </div>
      <h1 class="text-purple-matcha text-sm mt-2">Worth 10 likes, and {{user.first_name}} sees your extra interest</h1>
    </div>
    <div class="text-center p-8 border-b cursor-pointer relative">
      <DropdownDisplayChoice
        v-on:save-single-choice="saveSingleChoice"
        class="max-w-xs mx-auto"
        v-bind:name="'report'"
        v-bind:starting-option="'harassment'"
        v-bind:options="['harassment', 'bot', 'spam', 'inappropriate content']"></DropdownDisplayChoice>
      <h1 class="onboarding-sub-container-content-button-outline mx-auto">Report</h1>
    </div>
    <div class="text-center p-8 cursor-pointer">
      <h1 class="uppercase mx-auto">Block user</h1>
    </div>
  </div>
</template>

<script>
import DropdownDisplayChoice from '@/components/shared/DropdownDisplayChoice.vue';

export default {
  props: ['user'],
  components: {
    DropdownDisplayChoice,
  },
  data: () => ({
    userInterests: [],
  }),
  methods: {
    preferences() {
      if (this.user.orientation === 'heterosexual' && this.user.gender === 'male') {
        return 'women';
      }
      if (this.user.orientation === 'heterosexual' && this.user.gender === 'female') {
        return 'men';
      }
      if (this.user.orientation === 'homosexual' && this.user.gender === 'male') {
        return 'men';
      }
      if (this.user.orientation === 'homosexual' && this.user.gender === 'female') {
        return 'women';
      }
      if (this.user.orientation === 'bisexual') {
        return 'men & women';
      }
      if (this.user.orientation === 'other') {
        return 'genders other than men & women';
      }
      return 'any gender';
    },
    saveSingleChoice(...args) {
      const [key, value] = args;
      console.log(key);
      console.log(value);
    },
  },
  async beforeMount() {
    const sliderRangesRequest = await this.$http.get('/search/values');
    const maxScore = sliderRangesRequest.data.search_minmax.max_score;
    const sliderScore = document.getElementById('sliderScore');
    const sliderScoreWidth = `${sliderScore.getBoundingClientRect().width}px`;
    const marginLeft = `${(this.user.heat_score / maxScore) * 100}%`;
    if (this.user.heat_score / maxScore < 0.2) {
      sliderScore.style.marginLeft = `${marginLeft}`;
    } else {
      sliderScore.style.marginLeft = `calc(${marginLeft} - ${sliderScoreWidth})`;
    }
    const interests = this.user.tags;
    if (interests) {
      for (let j = 0; j < interests.length; j += 1) {
        this.userInterests.push(interests[j].name);
      }
    }
  },
};
</script>

<style scoped>
@screen md {
  .profileContainer {
    height: 75vh;
  }
}

.heatScore {
  background-image: linear-gradient(to right, #efedfd, #6246EA);
}

</style>
