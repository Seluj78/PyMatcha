<template>
  <!-- eslint-disable -->
  <div class="profileContainer md:overflow-scroll">
    <div class="text-center text-wrap p-8 md:pt-0 border-b">
      <h1 class="text-gray-matcha text-3xl font-semibold">{{user.first_name}}, {{user.age}}</h1>
      <div class="flex items-center text-left33">
        <img src="../../../assets/gender.png" class="w-4 h-4 mr-2">
        <h1 class="text-gray-matcha mt-4"><span class="capitalize">{{user.gender}}</span> looking for {{preferences()}}</h1>
      </div>
      <div class="flex items-center mt-2 text-left">
        <img src="../../../assets/location.png" class="w-4 h-4 mr-2">
        <h1 class="text-gray-matcha">42 km away</h1>
      </div>
    </div>
    <div class="text-center text-wrap p-8 border-b">
      <h1>{{user.bio}}</h1>
      <div class="flex flex-wrap justify-center mx-auto mt-6">
        <h1 v-for="(interest, index) in userInterests" :key="index"
        class="px-4 py-1 border rounded-xl mr-2 mt-2 text-gray-600">{{interest}}</h1>
      </div>
    </div>
    <div class="text-center text-wrap p-8 border-b">
      <h1>Last seen</h1>
      <h1>{{formattedLastSeenDate}}</h1>
    </div>
    <div class="text-center flex mx-auto p-8 border-b">
      <div class="w-8/12 border border-purple-matcha py-2 rounded-lg cursor-pointer">
        <img src="../../../assets/heart.png" class="mx-auto w-8 h-8">
      </div>
      <div class="w-4/12 border border-purple-matcha py-2 rounded-lg ml-4">
        <h1 class="mx-auto text-xl">{{user.heat_score}}</h1>
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
    height: 30rem;
  }
}
</style>
