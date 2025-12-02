<template>
  <div id="app">
    <CameraCapture />
  </div>
</template>

<script>
import CameraCapture from './CameraCapture.vue';

export default {
  components: {
    CameraCapture
  }
}
</script>

<style>
#app {
  text-align: center;
}
</style>