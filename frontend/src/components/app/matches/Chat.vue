<template>
  <!--  eslint-disable max-len -->
  <div class="chat md:w-full md:max-w-2xl md:shadow-md md:rounded-md md:p-4 md:flex md:flex-col md:justify-start">
    <div class="w-1/2 flex items-center justify-between ml-auto">
      <div v-if="user" class="-ml-6 text-center">
        <ChatUser v-bind:match="user"></ChatUser>
        <h1 class="text-gray-matcha opacity-75 text-sm">{{user.first_name}}</h1>
      </div>
      <div class="md:hidden cursor-pointer text-lg lg:text-2xl w-10 h-10 flex items-center justify-center"
           v-on:click="closeChat()">
        <h1 class="noSelect capitalize opacity-50">←</h1>
      </div>
    </div>
    <div class="messages rounded-md overflow-scroll pt-4 pb-2 w-full">
      <div
        v-bind:class="{
        'flex': true,
        'mt-1': true,
        'justify-start': message.to_id === loggedInUserId,
        'justify-end': message.to_id !== loggedInUserId}"
        v-for="message in messages" :key="message.id">
      <h1 v-if="message.to_id === loggedInUserId"
          class="py-2 px-4 rounded-t-md rounded-br-md bg-purple-matcha text-white-matcha">{{message.content}}</h1>
      <h1 v-else
          class="py-2 px-4 rounded-t-md rounded-bl-md bg-green-500 text-white-matcha">{{message.content}}</h1>
      </div>
    </div>
    <div class="send w-full flex items-stretch">
      <div class="w-10/12 h-full">
        <input type="text" v-model="message" placeholder="Message..." class="h-full w-full border border-gray-500 rounded-md px-3 py-1 focus:outline-none active:outline-none text-gray-matcha">
      </div>
      <div
        class="w-2/12 rounded-md flex justify-center items-center bg-purple-matcha cursor-pointer ml-2"
        v-on:click="sendMessage()">
        <img src="../../../assets/sendWhite.png" class="w-5 py-2">
      </div>
    </div>
  </div>
</template>

<script>
import ChatUser from '@/components/app/matches/ChatUser.vue';

export default {
  props: ['chatWithUserId'],
  components: {
    ChatUser,
  },
  data: () => ({
    messages: [],
    user: null,
    message: '',
    loggedInUserId: null,
  }),
  methods: {
    closeChat() {
      this.$emit('close-chat');
    },
    async sendMessage() {
      await this.$http.post('/messages/send', {
        to_uid: this.user.id.toString(),
        content: this.message,
      });
    },
  },
  async beforeMount() {
    const messagesRequest = await this.$http.get(`/conversations/${this.chatWithUserId}`);
    this.messages = messagesRequest.data.messages;
    const userRequest = await this.$http.get(`/users/${this.chatWithUserId}`);
    this.user = userRequest.data;
    this.loggedInUserId = this.$store.getters.getLoggedInUser.id;
  },
};
</script>

<style scoped>

.chat {
  height: 75vh;
}

@screen md {
  .chat {
    height: 85vh;
  }
}

.messages {
  height: 90%;
}

.send {
  height: 10%;
}
</style>
