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
    <div id="messageBox" v-if="messages" class="messages my-2 break-words overflow-scroll w-full">
      <div v-bind:class="{
        'text-left': message.to_id === loggedInUserId,
        'text-right': message.to_id !== loggedInUserId}"
         v-for="message in messages" :key="message.id">
        <h1
        v-bind:class="{
          'p-2': true,
          'px-4': true,
          'mt-2': true,
          'inline-block': true,
          'max-w-xs': true,
          'rounded-t-md': true,
          'rounded-br-md': message.to_id === loggedInUserId,
          'rounded-bl-md': message.to_id !== loggedInUserId,
          'bg-purple-matcha': message.to_id === loggedInUserId,
          'bg-green-500': message.to_id !== loggedInUserId,
          'text-white-matcha': true}"
        >{{message.content}}</h1>
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
    messages: null,
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
      this.messages.push({ to_id: this.chatWithUserId, content: this.message });
      this.message = '';
      this.$nextTick(() => {
        const messageBox = document.getElementById('messageBox');
        messageBox.scrollTop = messageBox.scrollHeight;
      });
    },
  },
  async beforeMount() {
    const messagesRequest = await this.$http.get(`/conversations/${this.chatWithUserId}`);
    this.messages = messagesRequest.data.messages;
    const userRequest = await this.$http.get(`/users/${this.chatWithUserId}`);
    this.user = userRequest.data;
    this.loggedInUserId = this.$store.getters.getLoggedInUser.id;
    this.$nextTick(() => {
      const messageBox = document.getElementById('messageBox');
      messageBox.scrollTop = messageBox.scrollHeight;
    });
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