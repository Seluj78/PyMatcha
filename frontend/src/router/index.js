import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import SignUp from '../views/auth/SignUp.vue';
import SignIn from '../views/auth/SignIn.vue';
import ForgotPassword from '../views/auth/ForgotPassword.vue';
import AccountVerified from '../views/auth/AccountVerified.vue';
import ResetPassword from '../views/auth/ResetPassword.vue';
import ResetPasswordError from '../views/auth/ResetPasswordError.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/accounts/signup',
    name: 'SignUp',
    component: SignUp,
  },
  {
    path: '/accounts/signin',
    name: 'SignIn',
    component: SignIn,
  },
  {
    path: '/accounts/password/forgot',
    name: 'ForgotPassword',
    component: ForgotPassword,
  },
  {
    path: '/accounts/password/reset',
    name: 'ResetPassword',
    component: ResetPassword,
  },
  {
    path: '/accounts/password/reseterror',
    name: 'ResetPasswordError',
    component: ResetPasswordError,
  },
  {
    path: '/accounts/verified',
    name: 'AccountVerified',
    component: AccountVerified,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
