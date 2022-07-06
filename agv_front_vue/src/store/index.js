import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import app from './modules/app'
import settings from './modules/settings'
import user from './modules/user'
import permission from '@/store/modules/permission'
import map from '@/store/modules/map'
import theme from '@/store/modules/theme'
Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    app,
    settings,
    user,
    permission,
    map,
    theme
  },
  getters
})

export default store
