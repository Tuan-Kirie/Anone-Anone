import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from "../router";

Vue.use(Vuex);


export default new Vuex.Store({
    state: {
        status: '',
        token: localStorage.getItem('token') || null,
        profileImg: '',
        user_id: localStorage.getItem('user_id') || null,
        username_pr: localStorage.getItem('username_pr') || null,
    },
    getters: {
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
    },
    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, token) {
            state.status = 'success';
            state.token = token;
        },
        short_data(state, user_id, username) {
            state.user_id = user_id;
            state.username = username;
        },
        auth_error(state) {
            state.status = 'error'
        },
        logout(state) {
            state.status = '';
            state.token = ''

        }
    },
    actions: {
        login({commit}, user) {
            return new Promise(((resolve, reject) => {
                commit('auth_request');
                axios.post('http://127.0.0.1:8000/api-token-auth/', user)
                    .then(resp => {
                        const token = resp.data.token;
                        localStorage.setItem('token', token);
                        commit('auth_success', token);
                        resolve(resp);
                        router.push({name: 'Profile'})
                    })
                    .catch(er => {
                        commit('auth_error');
                        localStorage.removeItem('token');
                        reject(er)
                    })
            }))
        },
        getShortData({commit}, token) {
            return new Promise(((resolve, reject) => {
                axios.get('http://127.0.0.1:8000/user/short/',
                    {headers: {'Authorization': "JWT " + token}})
                    .then(resp => {
                        const user_id = resp.data.id;
                        localStorage.setItem('user_id', user_id)
                        const username_pr = resp.data.username;
                        localStorage.setItem('username_pr', username_pr)
                        commit('short_data', user_id, username_pr);
                        resolve(resp);
                    })
                    .catch(er => {
                        reject(er)
                    })
            }))
        },
        logout({commit}) {
            return new Promise((resolve) => {
                commit('logout');
                localStorage.removeItem('token');
                localStorage.removeItem('username_pr');
                localStorage.removeItem('user_id');
                router.push({name: 'Home'});
                resolve()
            })
        },

    }
},)