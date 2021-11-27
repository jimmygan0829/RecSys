const state = {
    authToken:'',
    username:''
}

const mutations = {
    SET_AUTH_TOKEN(state,authToken){
        state.authToken = authToken
    },
    SET_USERNAME(state,username){
        state.username = username
    }
}

const actions = {
    setAuthToken({commit},authToken) {
        commit('SET_AUTH_TOKEN',authToken)
    },
    setUsername({commit},username) {
        commit('SET_USERNAME',username)
    },
}

export default {
    state,
    mutations,
    actions
}