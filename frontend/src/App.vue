<template>
  <v-app id="app">
    <!-- <router-view/> -->
    <AddPlace></AddPlace>
    <!-- <Sunriseset></Sunriseset> -->
    <Map></Map>
  </v-app>
</template>

<style>
  #app {
    width: 100vw;
    height: 100vh;
  }
</style>

<script>
import Sunriseset from './components/Sunriseset';
import Map from './components/Map';
import AddPlace from './components/AddPlace';
import axios from 'axios';
export default {
  name: 'App',

  components: {
    Sunriseset,
    Map,
    AddPlace
  },

  data: () => ({
    riseInfo: [],
    setInfo: [],
  }),
};
</script>
