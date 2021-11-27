import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router)

const mainPage = function(r) {
  require.ensure([], ()=> {
    r(require('../components/mainPage.vue'))
  },'mainPage')
}

const mainMovieRecommendation = function(r) {
  require.ensure([], ()=> {
    r(require('../components/MainMovieRecommendation.vue'))
  },'mainMovieRecommendation')
}

const login = function(r) {
  require.ensure([], ()=> {
    r(require('../components/login.vue'))
  },'login')
}

const register = function(r) {
  require.ensure([], ()=> {
    r(require('../components/register.vue'))
  },'register')
}


export default new Router({
  routes: [
    {
      path: '/',
      name: 'mainPage',
      component: mainPage
    },
    {
      path: '/movieIntro/:id',
      name: 'mainMovieRecommendation',
      component: mainMovieRecommendation
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
  ]
})
