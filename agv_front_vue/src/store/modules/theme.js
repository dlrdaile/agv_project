const state = {
  theme: 'chalk'
}
const mutations = {
  changeTheme(state) {
    if (state.theme === 'chalk') {
      state.theme = 'vintage'
    } else {
      state.theme = 'chalk'
    }
  }
}
const actions = {
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
