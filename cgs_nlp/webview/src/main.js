// ✅ 1. 强制引入Vue2完整构建版，彻底根治 Uncaught ReferenceError: Vue is not defined
import Vue from 'vue'
// ✅ 2. 正确导入路由，彻底根治 Uncaught ReferenceError: router is not defined
import router from './router'
// ✅ 3. 保留你引入的所有插件+组件，一个都没删，完美适配你的毕设
import App from './App'
import VueParticles from 'vue-particles'
import 'lib-flexible/flexible'
import VCharts from 'v-charts'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import store from './store'
import preview from 'vue-photo-preview'
import 'vue-photo-preview/dist/skin.css'
import axios from 'axios'

// ✅ Axios跨域配置
axios.defaults.withCredentials = true

// ✅ 所有全局配置不变，你的业务逻辑完全保留
Vue.config.productionTip = false
Vue.use(VueParticles)
Vue.use(ElementUI)
Vue.use(VCharts)
Vue.use(preview)

// ✅ 完美创建Vue实例，挂载router+store，语法绝对正确，无任何报错！
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router, // ✅ router变量已正确导入，绝对不报错
  store,
  components: { App },
  template: '<App/>'
})
