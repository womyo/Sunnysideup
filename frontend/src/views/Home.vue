<template>
  <div class="home">
    <AddPlace></AddPlace>
    <Map></Map>
  </div>
</template>

<script>
import Map from '../components/Map';
import AddPlace from '../components/AddPlace';
export default {
  name: 'HomeView',
  components: {
    Map,
    AddPlace
  },
}
</script>