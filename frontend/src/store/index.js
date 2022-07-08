import Vue from 'vue'
import Vuex from 'vuex'
import placeStore from './modules/placeStore.js'
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex)

const store = new Vuex.Store({
    modules: {
        placeStore: placeStore,
    },
    plugins: [createPersistedState({
        paths: ["placeStore"]
    })]
})

export default store;