import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import SignUp from '../views/auth/SignUp.vue';
import SignIn from '../views/auth/SignIn.vue';
import ForgotPassword from '../views/auth/ForgotPassword.vue';
import AccountVerified from '../views/auth/AccountVerified.vue';
import AccountVerifiedError from '../views/auth/AccountVerifiedError.vue';
import ResetPassword from '../views/auth/ResetPassword.vue';
import ResetPasswordError from '../views/auth/ResetPasswordError.vue';
import Onboarding from '../views/app/Onboarding.vue';
import Browse from '../views/app/Browse.vue';
import Search from '../views/app/Search.vue';
import Settings from '../views/app/Settings.vue';
import User from '../components/app/users/User.vue';
import History from '../views/app/History.vue';
import Matches from '../views/app/Matches.vue';
import SignOut from '../views/auth/SignOut.vue';
import NotFound from '../views/NotFound.vue';
import store from '../store/index';

Vue.use(VueRouter);

function loggedInRedirectBrowse(to, from, next) {
  if (store.getters.getLoggedInUser) {
    next('/browse');
  } else {
    next();
  }
}

function notLoggedInRedirectLogin(to, from, next) {
  if (store.getters.getLoggedInUser) {
    next();
  } else {
    next('/accounts/signin');
  }
}

function blockRepeatedOnboarding(to, from, next) {
  const user = store.getters.getLoggedInUser;
  if (user && user.is_profile_completed) {
    next('/browse');
  } else if (user && !user.is_profile_completed) {
    next();
  } else {
    next('/accounts/signin');
  }
}

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
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/accounts/signin',
    name: 'SignIn',
    component: SignIn,
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/accounts/password/forgot',
    name: 'ForgotPassword',
    component: ForgotPassword,
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/accounts/password/reset',
    name: 'ResetPassword',
    component: ResetPassword,
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/accounts/password/reseterror',
    name: 'ResetPasswordError',
    component: ResetPasswordError,
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/accounts/verify',
    name: 'AccountVerified',
    component: AccountVerified,
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/accounts/verify/error',
    name: 'AccountVerifiedError',
    component: AccountVerifiedError,
    beforeEnter: loggedInRedirectBrowse,
  },
  {
    path: '/onboarding',
    name: 'Onboarding',
    component: Onboarding,
    beforeEnter: blockRepeatedOnboarding,
  },
  {
    path: '/browse',
    name: 'Browse',
    component: Browse,
    beforeEnter: notLoggedInRedirectLogin,
    props: true,
  },
  {
    path: '/search',
    component: Search,
    name: 'Search',
    beforeEnter: notLoggedInRedirectLogin,
  },
  {
    path: '/settings',
    component: Settings,
    name: 'Settings',
    beforeEnter: notLoggedInRedirectLogin,
  },
  {
    path: '/users/:id',
    component: User,
    name: 'Users',
    beforeEnter: notLoggedInRedirectLogin,
  },
  {
    path: '/history',
    component: History,
    name: 'History',
    beforeEnter: notLoggedInRedirectLogin,
  },
  {
    path: '/matches',
    component: Matches,
    name: 'Matches',
    beforeEnter: notLoggedInRedirectLogin,
  },
  {
    path: '/accounts/signout',
    component: SignOut,
    name: 'SignOut',
    beforeEnter: notLoggedInRedirectLogin,
  },
  {
    path: '*',
    component: NotFound,
    name: 'NotFound',
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
