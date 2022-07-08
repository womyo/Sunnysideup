import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default {
    state: {
        riseInfo: [],
    },
    mutations: {
        getRiseInfo(state, payload) {
            state.riseInfo = payload
        }
    },
    getters:{
        storedRiseInfo(state) {
            return state.riseInfo;
        },
    },
    actions:{
        async getRiseInfo({ commit }) {
            await axios
                .get('/api/rise/')
                .then(response => {
                    console.log(response.data)
                    commit("getRiseInfo", response.data);
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}