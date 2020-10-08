<template>
  <!-- eslint-disable max-len -->
  <div class="w-full my-2">
    <ValidationObserver v-slot="{ handleSubmit, invalid }" class="w-full">
      <form @submit.prevent="handleSubmit(onSubmit)" class="w-full">
        <div class="flex justify-between items-center w-full">
          <h1 class="text-md font-bold capitalize text-gray-matcha">{{ name }}</h1>
          <input v-if="edit" type="submit" :disabled="invalid" value="Save"
                 v-bind:class="{'text-lg': true,'text-purple-matcha': true, 'bg-transparent': true, 'focus:outline-none': true, 'active:outline-none': true, 'opacity-50': invalid, 'cursor-pointer': !invalid}">
          <h1 v-if="!edit" v-on:click="startEditing()" class="cursor-pointer text-md text-purple-matcha">{{ buttonText }}</h1>
        </div>
        <div v-if="!edit && type !== 'password'"><h1 class="text-md opacity-50">{{ currentValue }}</h1></div>
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
          <ValidationProvider v-if="type === 'password'" name="Password" rules="required|min:6|validPassword" v-slot="{errors}">
            <input type="password" placeholder="Password" v-model="currentValue" class="matcha-input max-w-xs">
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
  }),
  methods: {
    startEditing() {
      this.edit = true;
    },
    onSubmit() {
      this.edit = false;
    },
    passwordErrorHandler(error) {
      if (!error || error === 'The Password field is required') {
        return error;
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
