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
    for (let i = 0; i < user.images.length; i += 1) {
      if (user.images[i].is_primary) {
        const primaryCopy = user.images[i];
        user.images.splice(i, 1);
        user.images.unshift(primaryCopy);
      }
    }
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
