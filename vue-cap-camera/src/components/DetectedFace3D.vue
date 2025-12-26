<template>
  <div>
    <video id="video" width="640" height="480" autoplay></video>
    <canvas id="overlay" width="640" height="480"></canvas>
    <div id="babylon-container" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script>
import * as BABYLON from '@babylonjs/core';
import * as faceapi from 'face-api.js';

export default {
  name: 'FaceDetectionBabylon',
  mounted() {
    this.initCamera();
    this.initBabylon();
  },
  methods: {
    async initCamera() {
      const video = document.getElementById('video');
      const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
      video.srcObject = stream;

      video.onloadedmetadata = async () => {
        video.play();
        await this.loadModels();
        this.startFaceDetection(video);
      };
    },
    async loadModels() {
      const MODEL_URL = '/models'; // Đường dẫn tới thư mục chứa mô hình

      await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
      await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
    },
    async startFaceDetection(video) {
      const canvas = document.getElementById('overlay');
      faceapi.matchDimensions(canvas, { width: video.width, height: video.height });

      setInterval(async () => {
        const detections = await faceapi.detectSingleFace(video).withFaceLandmarks();

        if (detections) {
          const resizedDetections = faceapi.resizeResults(detections, { width: video.width, height: video.height });
          canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
          faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

          this.update3DModel(resizedDetections); // Cập nhật mô hình 3D
        }
      }, 100);
    },
    initBabylon() {
      const canvas = document.getElementById("babylon-container");
      const engine = new BABYLON.Engine(canvas, true);
      const scene = new BABYLON.Scene(engine);

      // Tạo bóng tối
      const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);

      // Tạo hình cầu
      this.sphere = BABYLON.MeshBuilder.CreateSphere("sphere", { diameter: 2 }, scene);

      engine.runRenderLoop(() => {
        scene.render();
      });

      window.addEventListener("resize", () => {
        engine.resize();
      });
    },
    update3DModel(landmarks) {
      const points = landmarks.positions;

      // Dùng điểm mốc từ khuôn mặt để điều chỉnh hình cầu (sẽ cần thử nghiệm để đạt được hiệu ứng tốt nhất)
      this.sphere.position.x = points[30].x / 100; // Ví dụ sử dụng điểm mốc
      this.sphere.position.y = -points[30].y / 100; // Đảo ngược giá trị y nếu cần
    },
  },
};
</script>

<style>
#video {
  position: absolute;
  z-index: 1;
}

#overlay {
  position: absolute;
  z-index: 2;
}
</style>