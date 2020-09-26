/* eslint-disable no-shadow */

const state = {
  user: null,
};

const getters = {
  getLoggedInUser(state) {
    return state.user;
  },
};

const mutations = {
  login(state, user) {
    state.user = user;
  },
  logout(state) {
    state.user = null;
  },
  profileCompleted(state) {
    state.user.is_profile_completed = true;
  },
};

const actions = {
  login(state, user) {
    state.commit('login', user);
  },
  logout(state) {
    state.commit('logout');
  },
  profileCompleted(state) {
    state.commit('profileCompleted');
  },
};

export default {
  state,
  getters,
  mutations,
  actions,
};
