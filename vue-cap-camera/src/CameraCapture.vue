<template>
  <div class="face-detection">
    <video ref="video" autoplay muted playsinline width="720" height="560"></video>
    <canvas ref="canvas" style="display: none"></canvas>

    <div class="controls">
      <button @click="startCamera" :disabled="isRunning || loading">Bật camera</button>
      <button @click="stopCamera" :disabled="!isRunning">Tắt camera</button>
    </div>

    <p v-if="loading" style="color: orange;">Đang tải models (lần đầu hơi lâu ~10-20s)...</p>
    <p v-if="error" style="color: red;">Lỗi: {{ error }}</p>
    <p v-if="status" style="color: green; font-weight: bold;">{{ status }}</p>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import * as faceapi from '@vladmandic/face-api'

const video = ref(null)
const canvas = ref(null)
const isRunning = ref(false)
const loading = ref(false)
const error = ref('')
const status = ref('')

let stream = null
let detectInterval = null
let faceDetectedBefore = false  // Để chống spam log

const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/'

const loadModels = async () => {
  if (faceapi.nets.tinyFaceDetector.isLoaded) return // Đã load rồi thì thôi

  try {
    loading.value = true
    status.value = 'Đang tải models...'
    error.value = ''

    await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL)
    await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL)
    // Không cần faceRecognitionNet nếu chỉ detect
    console.log('Models loaded thành công!')
    status.value = 'Models đã sẵn sàng!'
  } catch (err) {
    error.value = 'Load model thất bại: ' + err.message
    console.error(err)
  } finally {
    loading.value = false
  }
}

const startCamera = async () => {
  await loadModels()
  if (error.value) return

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 720, height: 560, facingMode: 'user' },
      audio: false
    })

    video.value.srcObject = stream
    await video.value.play()

    isRunning.value = true
    status.value = 'Camera đã bật – Đang theo dõi khuôn mặt...'

    // Bắt đầu vòng lặp detect
    detectInterval = setInterval(detectFaces, 100) // 300ms là ổn, nhẹ
  } catch (err) {
    error.value = 'Không mở được camera: ' + err.message
  }
}

const detectFaces = async () => {
  if (!isRunning.value || !video.value?.videoWidth) return

  try {
    const detections = await faceapi.detectAllFaces(
        video.value,
        new faceapi.TinyFaceDetectorOptions({
          inputSize: 320,     // Nhẹ hơn, nhanh hơn
          scoreThreshold: 0.5
        })
    )

    const hasFace = detections.length > 0

    if (hasFace && !faceDetectedBefore) {
      // CHỈ LOG 1 LẦN KHI MỚI PHÁT HIỆN
      console.log('Đã phát hiện')
      status.value = 'Đã phát hiện khuôn mặt!'
      faceDetectedBefore = true
    } else if (!hasFace && faceDetectedBefore) {
      // Khi khuôn mặt biến mất
      status.value = 'Không thấy khuôn mặt...'
      faceDetectedBefore = false
    }
  } catch (err) {
    console.error('Lỗi detect:', err)
  }
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    video.value.srcObject = null
  }
  if (detectInterval) {
    clearInterval(detectInterval)
    detectInterval = null
  }

  isRunning.value = false
  faceDetectedBefore = false
  status.value = 'Camera đã tắt'
}

// Dọn dẹp khi component bị hủy
onUnmounted(() => {
  stopCamera()
})
</script>

<style scoped>
.face-detection {
  text-align: center;
  padding: 20px;
  font-family: system-ui, sans-serif;
  width: 950px;
}
video {
  border: 2px solid #333;
  border-radius: 12px;
  margin: 10px 0;
}
.controls button {
  margin: 8px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
}
</style>