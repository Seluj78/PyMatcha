<template>
  <!--  eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Matches'"></NavBar>
    <section class="mx-auto">
      <div>
        <div class="mt-8">
          <div v-if="matches.length">
            <h1 class="text-xl text-gray-matcha text-center font-bold">New matches</h1>
            <div class="overflow-scroll mt-4">
              <Match v-for="match in matches" :key="match.id" v-bind:match="match"></Match>
            </div>
          </div>
          <div v-else class="flex items-center">
            <div>
              <img src="../../assets/link.png" class="w-8 opacity-75">
            </div>
            <div class="ml-4">
              <h1 class="text-xl text-gray-matcha font-bold">No new matches</h1>
              <h1 class="text-sm text-gray-500">If someone likes you back, that user will appear here</h1>
            </div>
          </div>
        </div>
        <div class="mt-8">
          <div v-if="messages.length">
            <h1 class="text-xl text-gray-matcha text-center font-bold">Messages</h1>
            <div></div>
          </div>
          <div v-else class="flex items-center">
            <div>
              <img src="../../assets/chat.png" class="w-8 opacity-75">
            </div>
            <div class="ml-4">
              <h1 class="text-xl text-gray-matcha font-bold">No messages</h1>
              <h1 class="text-sm text-gray-500">Conversations with your matches will appear here</h1>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
/* eslint-disable max-len */
/* eslint-disable no-await-in-loop */

import NavBar from '@/components/shared/NavBar.vue';
import Match from '@/components/app/matches/Match.vue';

export default {
  name: 'Matches',
  components: {
    NavBar,
    Match,
  },
  data: () => ({
    matches: [],
    messages: [],
  }),
  methods: {
    async fetchMatches() {
      const matchesRequest = await this.$http.get('/matches');
      const { matches } = matchesRequest.data;
      for (let i = 0; i < matches.length; i += 1) {
        const userRequest = await this.$http.get(`/users/${matches[i].user_1}`);
        this.matches.push(userRequest.data);
      }
    },
    async fetchMessages() {
      const messagesRequest = await this.$http.get('/conversations');
      const messages = messagesRequest.data;
      for (let i = 0; i <= messages.length; i += 1) {
        const userChattingWith = await this.$http.get(`/users/${messages[i].with_user}`);
        messages[i].user = userChattingWith.data;
      }
      this.messages = messages;
    },
  },
  async beforeMount() {
    await this.fetchMatches();
    await this.fetchMessages();
  },
};
</script>
