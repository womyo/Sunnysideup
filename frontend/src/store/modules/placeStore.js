import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

const placeStore =  {
    namespace: true,
    state: {
        sunriseInfo: [],
        sunsetInfo: [],
    },
    mutations: {
        SE_SUNRISE_INFO (state, payload) {
            state.sunriseInfo = payload
        },
        SE_SUNSET_INFO(state, payload) {
            state.sunsetInfo = payload
        }
    },
    getters:{
        GE_SUNRISE_INFO (state) {
            return state.sunriseInfo;
        },
        GE_SUNSET_INFO (state) {
            return state.sunsetInfo;
        },
    },
    actions:{
        async SUNRISE_INFO ({ commit }) {
            await axios
                .get('/api/rise/')
                .then(response => {
                    commit("SE_SUNRISE_INFO", response.data);
                })
                .catch(error => {
                    console.log(error)
                })
        },
        async SUNSET_INFO ({ commit }) {
            await axios
                .get('/api/set/')
                .then(response => {
                    commit("SE_SUNSET_INFO", response.data);
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
export default placeStore;
