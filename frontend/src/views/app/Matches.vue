<template>
  <!--  eslint-disable max-len -->
  <div class="mx-4 sm:mx-16 lg:mx-32">
    <NavBar v-bind:currentRoute="'Matches'"></NavBar>
    <section v-if="fetchingDone" class="mx-auto relative md:flex md:items-start">
      <div class="md:w-full md:max-w-xs md:shadow-md md:rounded-md md:p-8 md:flex md:flex-col md:justify-start">
        <div class="mt-8 sm:mt-0">
          <div v-if="matches.length">
            <h1 class="text-xl md:text-base text-gray-matcha font-bold">Matches</h1>
            <div class="overflow-scroll mt-4">
              <Match v-on:chat="chat" v-for="match in matches" :key="match.id" v-bind:match="match"></Match>
            </div>
          </div>
          <div v-else class="flex items-center">
            <div>
              <img src="../../assets/link.png" class="w-8 opacity-75">
            </div>
            <div class="ml-4">
              <h1 class="text-xl md:text-base text-gray-matcha font-bold">Matches</h1>
              <h1 class="text-sm text-gray-500">If someone likes you back, that user will appear here</h1>
            </div>
          </div>
        </div>
        <div class="mt-8">
          <div v-if="messages.length">
            <h1 class="text-xl md:text-base text-gray-matcha text-center font-bold">Messages</h1>
            <div></div>
          </div>
          <div v-else class="flex items-center">
            <div>
              <img src="../../assets/chat.png" class="w-8 opacity-75">
            </div>
            <div class="ml-4">
              <h1 class="text-xl md:text-base text-gray-matcha font-bold">Messages</h1>
              <h1 class="text-sm text-gray-500">Conversations with your matches will appear here</h1>
            </div>
          </div>
        </div>
      </div>
      <Chat class="absolute top-0 w-full h-full bg-white-matcha
      md:relative md:ml-4"
            v-if="chatWithUserId"
            v-bind:chatWithUserId="chatWithUserId"
            v-on:close-chat="closeChat()"></Chat>
      <div v-if="!chatWithUserId" class="pl-8 w-full text-left max-w-2xl invisible md:visible md:relative md:ml-4">
        <div v-if="!matches.length && !messages.length">
          <h1 class="text-4xl text-gray-400 font-bold">Use Browse, Search</h1>
          <h1 class="text-4xl text-gray-400 font-bold">to like people</h1>
          <h1 class="text-4xl text-gray-400 font-bold">and get matches</h1>
        </div>
        <div v-if="matches.length && !messages.length">
          <h1 class="text-5xl text-gray-400 font-bold">Time to chat</h1>
          <h1 class="text-5xl text-gray-400 font-bold">with your</h1>
          <h1 class="text-5xl text-gray-400 font-bold">matches</h1>
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
import Chat from '@/components/app/matches/Chat.vue';

export default {
  name: 'Matches',
  components: {
    Chat,
    NavBar,
    Match,
  },
  data: () => ({
    matches: [],
    messages: [],
    chatWithUserId: null,
    fetchingDone: false,
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
    async chat(...args) {
      const [id] = args;
      if (id) {
        this.chatWithUserId = id;
      }
    },
    closeChat() {
      this.chatWithUserId = null;
    },
  },
  async beforeMount() {
    await this.fetchMatches();
    await this.fetchMessages();
    this.fetchingDone = true;
  },
};
</script>
