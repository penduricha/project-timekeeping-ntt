<template>
  <div id="app">
    <DetectedFace3D/>
  </div>
</template>

<script>
import CameraCapture from './CameraCapture.vue';
import CameraCaptureFirst from "@/CameraCaptureFirst.vue";
import DetectedFace3D from "@/components/DetectedFace3D.vue";

export default {
  components: {
    CameraCapture,
    CameraCaptureFirst,
    DetectedFace3D,
  }
}
</script>

<style>
#app {
  text-align: center;
}
</style>