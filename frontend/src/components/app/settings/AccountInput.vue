<template>
  <!-- eslint-disable max-len -->
  <div class="w-full my-4 max-w-sm">
    <ValidationObserver v-slot="{ handleSubmit, invalid }" class="w-full">
      <form @submit.prevent="handleSubmit(onSubmit)" class="w-full">
        <h1 v-if="error" class="focus:outline-none text-md font-bold capitalize text-red-500">{{ error }}</h1>
        <div class="flex justify-between items-center w-full">
          <h1 class="text-md font-bold capitalize text-gray-matcha">{{ name }}</h1>
          <div class="flex">
            <h1 v-if="edit" v-on:click="cancelEditing()" class="mr-4 text-sm text-purple-matcha cursor-pointer">Cancel</h1>
            <input v-if="edit" type="submit" :disabled="invalid || currentValue === currentValueBackup" value="Save"
                   v-bind:class="{'text-sm': true,'text-purple-matcha': true, 'bg-transparent': true, 'focus:outline-none': true, 'active:outline-none': true, 'opacity-50': invalid || currentValue === currentValueBackup, 'cursor-pointer': !invalid && currentValue !== currentValueBackup}">
            <h1 v-if="!edit" v-on:click="startEditing()" class="cursor-pointer text-sm text-purple-matcha">{{ buttonText }}</h1>
          </div>
        </div>
        <div v-on:click="startEditing()" class="break-words" v-if="!edit && type !== 'password'"><h1 class="text-md opacity-50 md:max-w-sm">{{ currentValue }}</h1></div>
        <div v-if="edit">
          <ValidationProvider v-if="type === 'firstName'" name="First Name" rules="required|alpha|max:20" v-slot="{errors}">
            <input type="text" placeholder="First Name" v-model="currentValue" class="matcha-input md:max-w-sm">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'lastName'" name="Last Name" rules="required|alpha|max:20" v-slot="{errors}">
            <input type="text" placeholder="Last Name" v-model="currentValue" class="matcha-input md:max-w-sm">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'email'" name="Email" rules="required|email|max:50" v-slot="{errors}">
            <input type="email" placeholder="Email" v-model="currentValue" class="matcha-input md:max-w-sm">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'username'" name="Username" rules="required|alpha_dash|max:20" v-slot="{errors}">
            <input type="text" placeholder="Username" v-model="currentValue" class="matcha-input md:max-w-sm">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'bio'" name="Biography" rules="required|min:51|max:200" v-slot="{errors}">
            <textarea style="resize: none;" rows="4" type="text" placeholder="Biography" v-model="currentValue" class="matcha-input md:max-w-sm block"></textarea>
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'password'" name="Current Password" rules="required" v-slot="{errors}">
            <input type="password" placeholder="Current Password" v-model="passwordOld" class="matcha-input md:max-w-sm">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'password'" name="Password" rules="required|min:6|validPassword" v-slot="{errors}">
            <input type="password" placeholder="New Password" v-model="currentValue" class="matcha-input md:max-w-sm mt-4">
            <span class="matcha-input-error">{{ passwordErrorHandler(errors[0]) }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'password'" name="Repeat Password" rules="required|confirmed:Password" v-slot="{errors}">
            <input type="password" placeholder="Repeat New Password" v-model="passwordRepeat" class="matcha-input">
            <span class="matcha-input-error">{{ passwordErrorHandler(errors[0]) }}</span>
          </ValidationProvider>
        </div>
      </form>
    </ValidationObserver>
  </div>
</template>

<script>
export default {
  props: ['name', 'type', 'currentValuePassed'],
  data: () => ({
    edit: false,
    currentValueBackup: '',
    currentValue: '',
    passwordRepeat: '',
    passwordOld: '',
    error: '',
  }),
  methods: {
    startEditing() {
      this.error = '';
      this.currentValueBackup = this.currentValue;
      this.edit = true;
    },
    cancelEditing() {
      if (this.type === 'password') {
        this.currentValue = '';
        this.passwordRepeat = '';
        this.passwordOld = '';
      }
      this.currentValue = this.currentValueBackup;
      this.edit = false;
    },
    async onSubmit() {
      this.error = false;
      this.edit = false;
      this.currentValueBackup = this.currentValue;
      try {
        if (this.type === 'firstName') {
          await this.$http.patch('/profile/edit/first_name', { first_name: this.currentValue }, { accessTokenRequired: true });
        } else if (this.type === 'lastName') {
          await this.$http.patch('/profile/edit/last_name', { last_name: this.currentValue }, { accessTokenRequired: true });
        } else if (this.type === 'email') {
          await this.$http.put('/profile/edit/email', { email: this.currentValue }, { accessTokenRequired: true });
        } else if (this.type === 'username') {
          await this.$http.patch('/profile/edit/username', { username: this.currentValue }, { accessTokenRequired: true });
        } else if (this.type === 'bio') {
          await this.$http.patch('/profile/edit/bio', { bio: this.currentValue }, { accessTokenRequired: true });
        } else if (this.type === 'password') {
          await this.$http.put('/profile/edit/password', {
            old_password: this.passwordOld,
            new_password: this.currentValue,
          }, { accessTokenRequired: true });
          this.currentValue = '';
          this.passwordRepeat = '';
          this.passwordOld = '';
        }
        const user = await this.$http.get(`/users/${this.$store.getters.getLoggedInUser.id}`, { accessTokenRequired: true });
        await this.$store.dispatch('login', user.data);
      } catch (error) {
        this.error = error.response.data.error.message;
        if (this.type === 'password') {
          this.currentValue = '';
          this.passwordRepeat = '';
          this.passwordOld = '';
        }
      }
    },
    passwordErrorHandler(error) {
      if (!error || error === 'The Password field is required' || error === 'The Repeat Password field is required') {
        return error;
      }
      if (error === 'The Repeat Password field confirmation does not match') {
        return 'Passwords do not match';
      }
      return 'This password is too easy to guess';
    },
  },
  computed: {
    buttonText() {
      if (this.edit) {
        return 'Save';
      }
      return 'Edit';
    },
  },
  beforeMount() {
    this.currentValue = this.currentValuePassed;
  },
};
</script>
