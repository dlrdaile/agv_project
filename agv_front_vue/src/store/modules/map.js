import { getMapList } from '@/api/map'

const state = {
  mapList: []
}

const mutations = {
  SET_MAPLIST: (state, maplist) => {
    // eslint-disable-next-line no-prototype-builtins
    state.mapList = maplist
  },
  CLEAR_MAPLIST: (state) => {
    state.mapList = []
  }
}

const actions = {
  GetMapList({ commit }) {
    return getMapList()
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
