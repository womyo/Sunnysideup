<template>
  <div class="place">
    <EditPlace></EditPlace>
    <PlaceDetail></PlaceDetail>
  </div>
</template>

<script>
import PlaceDetail from '../components/PlaceDetail';
import EditPlace from '../components/EditPlace';

export default {
  name: 'PlaceView',
  components: {
    PlaceDetail,
    EditPlace,
  },
}
</script>