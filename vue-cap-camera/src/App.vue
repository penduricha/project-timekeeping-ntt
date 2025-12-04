<template>
  <div id="app">
    <CameraCapture/>
  </div>
</template>

<script>
import CameraCapture from './CameraCapture.vue';
import CameraCaptureFirst from "@/CameraCaptureFirst.vue";

export default {
  components: {
    CameraCapture,
    CameraCaptureFirst
  }
}
</script>

<style>
#app {
  text-align: center;
}
</style>