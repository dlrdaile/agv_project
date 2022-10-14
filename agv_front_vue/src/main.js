import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css
import '@/assets/css/global.css'
import '@/assets/css/font.css'
import App from './App'
import store from './store'
import router from './router'

import '@/icons' // icon
import '@/permission' // permission control
import config from '@/config'
import VueQuillEditor from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'

import dataV from '@jiaminghi/data-view'

// 导入订单的监控仪表盘
import '@/assets/font/iconfont.css'
import SocketService from '@/utils/socket_service'
import VueCropper from 'vue-cropper'
/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../mock')
  mockXHR()
}

// set ElementUI lang to EN
// Vue.use(ElementUI, { locale })
// 如果想要中文版 element-ui，按如下方式声明
Vue.use(ElementUI)
Vue.use(VueQuillEditor)
Vue.use(dataV)
Vue.use(VueCropper)
Vue.config.productionTip = false
Vue.prototype.$echarts = window.echarts
// 其他的组件  this.$socket
Vue.prototype.$socket = SocketService.Instance
Vue.prototype.$bus = new Vue()
Vue.prototype.$localUrl = `http://${config.baseUrl}:${config.basePort}`
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
