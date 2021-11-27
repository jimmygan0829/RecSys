// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import Vuex from 'vuex'
import storeObj from '../src/store'


Vue.prototype.$axios = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000' 
Vue.config.productionTip = false
Vue.use(ElementUI);
Vue.use(Vuex)
const store = new Vuex.Store(storeObj)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})