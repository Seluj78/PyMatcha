<template>
  <!-- eslint-disable max-len -->
  <div class="w-full my-4">
    <ValidationObserver v-slot="{ handleSubmit, invalid }" class="w-full">
      <form @submit.prevent="handleSubmit(onSubmit)" class="w-full">
        <div class="flex justify-between items-center w-full">
          <h1 class="text-md font-bold capitalize text-gray-matcha">{{ name }}</h1>
          <input v-if="edit" type="submit" :disabled="invalid" value="Save"
                 v-bind:class="{'text-sm': true,'text-purple-matcha': true, 'bg-transparent': true, 'focus:outline-none': true, 'active:outline-none': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
          <h1 v-if="!edit" v-on:click="startEditing()" class="cursor-pointer text-sm text-purple-matcha">{{ buttonText }}</h1>
        </div>
        <div class="break-words" v-if="!edit && type !== 'password'"><h1 class="text-md opacity-50 max-w-xs">{{ currentValue }}</h1></div>
        <div v-if="edit">
          <ValidationProvider v-if="type === 'firstName'" name="First Name" rules="required|alpha|max:20" v-slot="{errors}">
            <input type="text" placeholder="First Name" v-model="currentValue" class="matcha-input max-w-xs">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'lastName'" name="Last Name" rules="required|alpha|max:20" v-slot="{errors}">
            <input type="text" placeholder="Last Name" v-model="currentValue" class="matcha-input max-w-xs">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'email'" name="Email" rules="required|email|max:50" v-slot="{errors}">
            <input type="email" placeholder="Email" v-model="currentValue" class="matcha-input max-w-xs">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'username'" name="Username" rules="required|alpha_dash|max:20" v-slot="{errors}">
            <input type="text" placeholder="Username" v-model="currentValue" class="matcha-input max-w-xs">
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'bio'" name="Biography" rules="required|min:50|max:200" v-slot="{errors}">
            <textarea style="resize: none;" rows="4" type="text" placeholder="Biography" v-model="currentValue" class="matcha-input max-w-xs block"></textarea>
            <span class="matcha-input-error">{{ errors[0] }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'password'" name="Password" rules="required|min:6|validPassword" v-slot="{errors}">
            <input type="password" placeholder="New Password" v-model="currentValue" class="matcha-input max-w-xs">
            <span class="matcha-input-error">{{ passwordErrorHandler(errors[0]) }}</span>
          </ValidationProvider>
          <ValidationProvider v-if="type === 'password'" name="Repeat Password" rules="required|confirmed:Password" v-slot="{errors}">
            <input type="password" placeholder="Repeat Password" v-model="passwordRepeat" class="matcha-input mt-4">
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
    currentValue: '',
    passwordRepeat: '',
  }),
  methods: {
    startEditing() {
      this.edit = true;
    },
    onSubmit() {
      if (this.type === 'password') {
        this.currentValue = '';
        this.passwordRepeat = '';
      }
      this.edit = false;
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