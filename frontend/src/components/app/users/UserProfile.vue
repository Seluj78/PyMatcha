<template>
  <!-- eslint-disable -->
  <div class="profileContainer">
    <div class="text-center text-wrap p-8 border-b">
      <h1 class="text-gray-matcha text-3xl font-semibold mb-6">{{user.first_name}}, {{user.age}}</h1>
      <div v-if="!user.is_online" class="flex items-center mt-2 text-left">
        <img class="w-3 h-3 mr-2" src="../../../assets/recommendations/offline.png">
        <h1 class="text-gray-600">Last seen {{formattedLastSeenDate}}</h1>
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
    <div class="text-center flex mx-auto p-8 border-b">
      <div class="w-full border border-purple-matcha py-2 rounded-lg cursor-pointer">
        <img src="../../../assets/heart.png" class="mx-auto w-8 h-8">
      </div>
    </div>
    <div class="text-center p-8 border-b cursor-pointer">
      <h1 class="uppercase mx-auto">Block user</h1>
    </div>
    <div class="text-center p-8 cursor-pointer">
      <h1 class="uppercase mx-auto">Report as fake</h1>
    </div>
  </div>
</template>

<script>
export default {
  props: ['user'],
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
  },
  computed: {
    formattedLastSeenDate() {
      if (this.user.date_lastseen) {
        return this.user.date_lastseen.slice(0, -7);
      }
      return undefined;
    },
  },
  beforeMount() {
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
</style>
