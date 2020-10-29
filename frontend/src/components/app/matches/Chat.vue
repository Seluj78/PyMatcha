<template>
  <!--  eslint-disable max-len -->
  <div class="chat md:w-full md:max-w-2xl md:shadow-md md:rounded-md md:p-4 md:flex md:flex-col md:justify-start">
    <div class="flex items-center justify-center">
      <div v-if="user" class="text-center flex-row">
        <ChatUser class="mx-auto" v-bind:match="user"></ChatUser>
        <h1 class="text-gray-matcha opacity-75 text-sm">{{user.first_name}}</h1>
      </div>
      <div class="md:hidden absolute right-0 cursor-pointer text-lg lg:text-2xl w-10 h-10 flex items-center justify-center"
           v-on:click="closeChat()">
        <h1 class="noSelect capitalize opacity-50">←</h1>
      </div>
    </div>
    <div id="messageBox" v-if="messages" class="messages my-2 break-words overflow-scroll w-full">
      <div v-bind:class="{
        'text-left': message.to_id === loggedInUserId,
        'text-right': message.to_id !== loggedInUserId}"
         v-for="(message, index) in messages" :key="index">
        <div v-if="message.first_in_timespan"
             v-bind:class="{'text-center': true, 'mx-auto': true, 'mt-8': index !== 0}">
          <h1
            class="text-sm inline-block rounded-md bg-gray-200 px-2 py-1">{{message.timestamp_first}}</h1>
        </div>
        <MessageBubble
          v-bind:loggedInUserId="loggedInUserId"
          v-bind:messagePassed="message"></MessageBubble>
      </div>
    </div>
    <form v-on:submit.prevent="sendMessage()" class="send w-full flex items-stretch">
      <div class="w-10/12 h-full">
        <input type="text" v-model="message" placeholder="Message..." class="h-full w-full border border-gray-500 rounded-md px-3 py-1 focus:outline-none active:outline-none text-gray-matcha">
      </div>
      <button type="submit"
        class="w-2/12 rounded-md flex justify-center items-center bg-purple-matcha cursor-pointer ml-2">
        <img src="../../../assets/sendWhite.png" class="w-5 py-2">
      </button>
    </form>
  </div>
</template>

<script>
/* eslint-disable no-param-reassign */
import ChatUser from '@/components/app/matches/ChatUser.vue';
import MessageBubble from '@/components/app/matches/MessageBubble.vue';

export default {
  props: ['chatWithUserId'],
  components: {
    ChatUser,
    MessageBubble,
  },
  data: () => ({
    messages: null,
    user: null,
    message: '',
    loggedInUserId: null,
    fetchMessagesIntervalId: null,
    latestMessagesDate: null,
  }),
  methods: {
    determineFirstMessagesOfTimespans(messages) {
      const len = messages.length;
      for (let i = 0; i < len; i += 1) {
        if (this.displayDate(messages[i].timestamp)) {
          messages[i].first_in_timespan = true;
          messages[i].timestamp_first = this.getDayMonthday(messages[i].timestamp);
        } else {
          messages[i].first_in_timespan = false;
        }
      }
    },
    getDayMonthday(timestamp) {
      const splitBySpace = timestamp.split(' ');
      return `${splitBySpace[0]} ${splitBySpace[1]} ${splitBySpace[2]}`;
    },
    displayDate(timestamp) {
      const dayMonthday = this.getDayMonthday(timestamp);
      if (dayMonthday !== this.latestMessagesDate) {
        this.latestMessagesDate = dayMonthday;
        return (1);
      }
      return (0);
    },
    scrollChatToBottom() {
      this.$nextTick(() => {
        const messageBox = document.getElementById('messageBox');
        if (messageBox) {
          messageBox.scrollTop = messageBox.scrollHeight;
        }
      });
    },
    closeChat() {
      this.$emit('close-chat');
    },
    async sendMessage() {
      if (!this.message.length) {
        return;
      }
      const response = await this.$http.post('/messages/send', {
        to_uid: this.user.id.toString(),
        content: this.message,
      });
      this.messages.push(response.data.new_message);
      this.message = '';
      this.$emit('new-message');
      this.scrollChatToBottom();
    },
    async fetchNewMessages() {
      const messagesRequest = await this.$http.get(`/conversations/${this.chatWithUserId}`);
      const newMessages = messagesRequest.data.messages;
      if (newMessages.length > this.messages.length) {
        for (let i = this.messages.length; i < newMessages.length; i += 1) {
          this.messages.push(newMessages[i]);
        }
        this.$emit('new-message');
        this.scrollChatToBottom();
      }
    },
    async prepareChatForNewUser() {
      const messagesRequest = await this.$http.get(`/conversations/${this.chatWithUserId}`);
      this.messages = messagesRequest.data.messages;
      this.determineFirstMessagesOfTimespans(this.messages);
      const userRequest = await this.$http.get(`/users/${this.chatWithUserId}`);
      this.user = userRequest.data;
      this.scrollChatToBottom();
    },
  },
  watch: {
    chatWithUserId: {
      async handler() {
        if (this.chatWithUserId) {
          await this.prepareChatForNewUser();
        }
      },
    },
  },
  async beforeMount() {
    await this.prepareChatForNewUser();
    this.loggedInUserId = this.$store.getters.getLoggedInUser.id;
    this.fetchMessagesIntervalId = setInterval(this.fetchNewMessages, 2000);
  },
  beforeDestroy() {
    window.clearInterval(this.fetchMessagesIntervalId);
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
