<template>
  <div>
    <video ref="video" autoplay></video>
    <button @click="takeSnapshot">Chụp Ảnh</button>
    <input type="file" @change="handleImageUpload" accept="image/*" />
    <canvas ref="canvas" style="display: none;"></canvas>
    <img v-if="imageSrc" :src="imageSrc" alt="Captured Image" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      imageSrc: ''  // Variable to hold Base64 string
    };
  },
  mounted() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.$refs.video.srcObject = stream;
        });
  },
  methods: {
    takeSnapshot() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');

      // Set canvas size
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;

      // Draw video image to canvas
      context.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

      // Convert canvas to Base64 string
      this.imageSrc = canvas.toDataURL('image/png');
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file && file.type.substr(0, 5) === 'image') {
        const reader = new FileReader();
        reader.onloadend = () => {
          this.imageSrc = reader.result;  // Convert to Base64
          console.log(this.imageSrc)
        };
        reader.readAsDataURL(file);
      }
    }
  }
}
</script>

<style>
video {
  width: 100%;
}
canvas {
  display: none;
}
img {
  display: block;
  margin-top: 10px;
  max-width: 100%; /* Ensure image displays correctly */
}
input[type="file"] {
  margin-top: 10px; /* Space between button and input */
}
</style>