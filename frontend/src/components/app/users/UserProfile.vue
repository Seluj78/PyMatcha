<template>
  <!-- eslint-disable max-len -->
  <div class="profileContainer relative">
    <div id="sliderScoreContainer" class="text-center w-full rounded-lt-md heatScore relative h-6">
      <div @mouseover="showScoreExplanation = true" @click="showScoreExplanation = true" id="sliderScore" class="cursor-default bg-purple-matcha absolute top-0 flex flex-col items-center justify-center h-12 w-auto rounded-b-md">
        <h1 class="text-white-matcha px-2">{{user.heat_score}}</h1>
      </div>
    </div>
    <div v-if="showScoreExplanation" @mouseleave="showScoreExplanation = false" @click="showScoreExplanation = false" class="absolute w-full top-0 h-16 flex text-center items-center justify-center sm:rounded-b-md md:rounded-b-none bg-purple-matcha z-20">
      <h1 class="text-white-matcha cursor-default p-2">Score based on likes, matches, messages count</h1>
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
      <LikeButton
        v-if="!likeButtons.superLikeClicked"
        v-bind:name="'like'"
        v-bind:startImage="likeImage"
        v-bind:hoverImage="likeImageHover"
        v-bind:clickedImage="likeImageClicked"
        v-bind:text="'Like'"
        v-bind:textRevert="'Unlike'"
        v-on:clicked="buttonClicked"
        v-on:revert="buttonRevert"></LikeButton>
      <LikeButton
        v-if="!likeButtons.likeClicked && superLikesLeft()"
        v-bind:name="'superLike'"
        v-bind:class="{'mt-8': !likeButtons.superLikeClicked}"
        v-bind:startImage="superLikeImage"
        v-bind:hoverImage="superLikeImageHover"
        v-bind:clickedImage="superLikeImageClicked"
        v-bind:text="'Super Like'"
        v-bind:textRevert="'Unlike'"
        v-bind:description="`Worth 10 likes, and ${user.first_name} sees your extra interest`"
        v-on:clicked="buttonClicked"
        v-on:revert="buttonRevert"></LikeButton>
    </div>
    <div class="text-center p-8 border-b relative">
      <DropdownDisplayChoice
        v-on:save-single-choice="saveSingleChoice"
        class="max-w-xs mx-auto"
        v-bind:name="'report'"
        v-bind:position="'center'"
        v-bind:starting-option="'harassment'"
        v-bind:options="['harassment', 'bot', 'spam', 'inappropriate content']"></DropdownDisplayChoice>
      <h1 v-on:click="makeReport()" class="onboarding-sub-container-content-button-outline mx-auto">Report</h1>
    </div>
    <div class="text-center p-8">
      <h1
        v-on:click="block()"
        class="onboarding-sub-container-content-button-outline text-red-500 mt-0 border-red-500 mx-auto">Block</h1>
      <h1 class="mx-auto mt-2 text-sm text-gray-600">Don't suggest this user and stop notifications</h1>
    </div>
  </div>
</template>

<script>
import DropdownDisplayChoice from '@/components/shared/DropdownDisplayChoice.vue';
import LikeButton from '@/components/app/users/LikeButton.vue';
import likeImage from '../../../assets/like.png';
import likeImageHover from '../../../assets/likeHover.png';
import likeImageClicked from '../../../assets/likeClicked.png';
import superLikeImage from '../../../assets/superLike.png';
import superLikeImageHover from '../../../assets/superLikeImageHover.png';
import superLikeImageClicked from '../../../assets/superLikeImageClicked.png';

export default {
  props: ['user'],
  components: {
    LikeButton,
    DropdownDisplayChoice,
  },
  data: () => ({
    userInterests: [],
    showScoreExplanation: false,
    likeImage,
    likeImageHover,
    likeImageClicked,
    superLikeImage,
    superLikeImageHover,
    superLikeImageClicked,
    likeButtons: {
      likeClicked: false,
      superLikeClicked: false,
    },
    report: 'harassment',
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
    superLikesLeft() {
      return true;
    },
    async buttonClicked(...args) {
      const [name] = args;
      if (name === 'like') {
        await this.$http.post(`/like/${this.user.id}`, { is_superlike: false });
        this.likeButtons.likeClicked = true;
      } else if (name === 'superLike') {
        await this.$http.post(`/like/${this.user.id}`, { is_superlike: true });
        this.likeButtons.superLikeClicked = true;
      }
    },
    async buttonRevert(...args) {
      const [name] = args;
      if (name === 'like') {
        await this.$http.post(`/unlike/${this.user.id}`, { is_superlike: false });
        this.likeButtons.likeClicked = false;
      } else if (name === 'superLike') {
        await this.$http.post(`/unlike/${this.user.id}`, { is_superlike: true });
        this.likeButtons.superLikeClicked = false;
      }
    },
    saveSingleChoice(...args) {
      const [key, value] = args;
      if (key === 'report') {
        this[key] = value;
      }
    },
    async makeReport() {
      await this.$http.post(`/profile/report/${this.user.id}`, { reason: this.report });
    },
    async block() {
      return true;
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
