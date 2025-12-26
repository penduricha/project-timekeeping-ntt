<script>
import AsideMenu from "@/components/aside/aside-menu/AsideMenu.vue";
import './timekeeping-camera.scss';
import RouterManagement from "@/routers/RouterManagement.js";
import ButtonBlue from "@/components/button/button-blue/ButtonBlue.vue";
import TextInvalid from "@/components/span/TextInvalid.vue";
import TransformText from "@/others/TransformText.js";
import TextSuccess from "@/components/span/TextSuccess.vue";

// run npm i @vladmandic/face-api: Library detected face
// import thư viện cần thiết

import * as faceapi from '@vladmandic/face-api'


export default {
  name: "TimeKeepingCamera",

  components: {
    ButtonBlue,
    AsideMenu,
    TextInvalid,
    TextSuccess,
  },

  data() {
    return {
      buttonTakeScreenShot: {
        btnDisable: false,
        btnText: "Open camera",
        btnLoading: false,
      },

      buttonResetData: {
        btnDisable: false,
        btnText: "Reset data",
        btnLoading: false,
      },

      employee: {
        employeeID: 1000,
        employeeName: 'Tu Quang Nhat',
        gender: true,
        position: 'Dev fullstack'
      },

      //parameters about camera
      statusCamera: '',
      statusSuccess: true,
      statusError: false,
      currentStream: null,
      detectInterval: null,
      //video: null,
      faceDetectedBefore: false,

      //frame khuôn mat
      currentFaceBox: null, // lưu box hiện tại để di chuyển khung
      faceStableCount: 0,   // đếm frame ổn định (tùy chọn)

      //image to post
      imageSrc: null,

      //hàm vẽ khung xanh
      //isDrawGreenFame: false,
    }
  },

  props: {},

  created() {
    //set path
    this.saveRouterPath(this.getRoute());
    this.setTitlePage();
  },

  mounted() {
    //this.setCameraComputer();
  },

  beforeUnmount() {
    this.closeCameraComputer();
  },

  methods: {
    setTitlePage() {
      document.title = 'Take a photo to check attendance';
    },

    async openCameraComputer() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {width: 720, height: 560, facingMode: 'user'},
          audio: false
        })

        this.$refs.video.srcObject = stream
        this.currentStream = stream
        await this.$refs.video.play();
        this.buttonTakeScreenShot.btnText = "Close camera";
      } catch (error) {
        alert(error.message);
      }
    },

    async closeCameraComputer() {
      if (this.currentStream) {
        const tracks = this.currentStream.getTracks();
        tracks.forEach(track => track.stop()); // Dừng tất cả các track
        this.$refs.video.srcObject = null; // Đặt srcObject về null
        this.currentStream = null; // Xóa stream đã lưu

      }
      await new Promise(resolve => setTimeout(resolve, 200));
      this.buttonTakeScreenShot.btnText = "Open camera";
      this.resetCameraParameters();
    },

    resetCameraParameters() {
      if (this.statusCamera !== '') {
        this.statusCamera = '';
      }
      this.statusSuccess = true;
      this.statusError = false;
      //this.video = null;
      this.currentStream = null;
      this.faceDetectedBefore = false;
      this.detectInterval = null;
      this.imageSrc = null;
      this.faceStableCount = 0;
    },

    getGenderFromBoolean(genderBoolean) {
      const transformText = new TransformText();
      return transformText.getGenderFromBoolean(genderBoolean);
    },

    getRoute() {
      //ở đây có props thì phải thêm path của props
      return this.$route.path;
    },

    saveRouterPath(route) {
      const routerManagement = new RouterManagement();
      routerManagement.savePathToSessionStorage(route);
    },

    //hàm chụp khuôn mặt
    async checkTextButtonToToggle() {
      if (this.buttonTakeScreenShot.btnText === "Open camera") {
        await this.startOpenCamera();
      } else if (this.buttonTakeScreenShot.btnText === "Close camera") {
        await this.stopCamera();
      }
    },

    async loadModelsFaceDetected() {
      const model_url = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/';
      if (faceapi.nets.tinyFaceDetector.isLoaded) {
        return;
      }
      try {
        this.statusCamera = 'Loading models...';
        await faceapi.nets.tinyFaceDetector.loadFromUri(model_url)
        await faceapi.nets.faceLandmark68Net.loadFromUri(model_url)
        // Không cần faceRecognitionNet nếu chỉ detect
        //console.log('Models loaded thành công!')
        //this.statusCamera = 'Face detection system is ready.';
      } catch (err) {
        this.statusCamera = err.message;
        this.statusError = true;
        this.statusSuccess = false;
        console.error(err)
      }
    },

    async takeSnapShot() {
      const canvas = this.$refs.canvas;
      const context = canvas.getContext('2d');

      // Set canvas size
      canvas.width = this.$refs.video.videoWidth;
      canvas.height = this.$refs.video.videoHeight;

      // Draw video image to canvas
      context.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);

      // Convert canvas to Base64 string
      this.imageSrc = canvas.toDataURL('image/png');
      console.log('Image src base64:', this.imageSrc)
      if (this.imageSrc) {
        //gọi cho API
      }
    },

    drawGreenFrame(video, tracker, detections) {
      // Vẽ khung hình xanh liên tục
      const detection = detections[0];
      const box = detection.box;

      // Tính tỷ lệ thực tế giữa video stream và vùng hiển thị
      //const videoRect = video.getBoundingClientRect();
      const displayWidth = video.offsetWidth;
      const displayHeight = video.offsetHeight;

      const scaleX = displayWidth / video.videoWidth;
      const scaleY = displayHeight / video.videoHeight;
      const scale = Math.max(scaleX, scaleY); // vì object-fit: contain/cover

      const offsetX = (displayWidth - video.videoWidth * scale) / 2;
      const offsetY = (displayHeight - video.videoHeight * scale) / 2;

      // Tọa độ chính xác trên màn hình
      const x = offsetX + box.x * scale;
      const y = offsetY + box.y * scale;
      const width = box.width * scale;
      const height = box.height * scale;

      // Cập nhật vị trí khung tracker
      this.currentFaceBox = {x, y, width, height};

      tracker.style.transform = `translate(${x + width / 2}px, ${y + height / 2}px)`;
      tracker.style.width = `${width + 40}px`;
      tracker.style.height = `${height + 60}px`;
    },

    async detectedFace() {
      const video = this.$refs.video;
      const tracker = this.$refs.faceTracker;

      if (!video || video.readyState < 2 || !video.videoWidth || !tracker) {
        this.currentFaceBox = null;
        return;
      }

      try {
        const detections = await faceapi.detectAllFaces(
            video,
            new faceapi.TinyFaceDetectorOptions({
              inputSize: 320,
              scoreThreshold: 0.5
            })
        );

        if (detections.length > 0) {
          // Lấy khuôn mặt có độ tin cậy cao nhất
          // Cập nhật trạng thái
          this.drawGreenFrame(video, tracker, detections);
          if (!this.faceDetectedBefore) {
            this.statusCamera = 'Detected face.';
            this.statusSuccess = true;
            this.statusError = false;
            this.faceDetectedBefore = true;
          }
          // Delay for 300 milliseconds
          await new Promise(resolve => setTimeout(resolve, 200));
          await this.takeSnapShot();
          this.faceDetectedBefore = false;
        } else {
          // Không thấy mặt → ẩn khung
          this.currentFaceBox = null;
          this.statusCamera = 'Can not detect face.';
          this.statusSuccess = false;
          this.statusError = true;
          this.faceDetectedBefore = false;
        }
      } catch (err) {
        console.error('Lỗi detect face:', err);
        this.currentFaceBox = null;
      }
    },

    async startOpenCamera() {
      try {
        //liên kết camera
        await this.openCameraComputer();
        //load models
        await this.loadModelsFaceDetected();
        // 1/10 giây
        this.detectInterval = setInterval(this.detectedFace, 200);
      } catch (err) {
        // error.value = 'Không mở được camera: ' + err.message
        alert(err);
      }
    },

    async stopCamera() {
      //this.resetCameraParameters();
      try {
        //liên kết camera
        await this.closeCameraComputer();
      } catch (err) {
        // error.value = 'Không mở được camera: ' + err.message
        alert(err);
      }
    },
  },

  setup()
  {

  },

  computed: {

  }
}
</script>

<template>
  <section class="section-time-keeping-camera">
    <AsideMenu/>
    <main class="main-time-keeping-camera">
      <div class="box-camera-and-employee">
        <div class="box-camera-take-photo">
          <div class="style-video-camera">
            <video
                ref="video"
                muted
                playsinline
                autoplay
                class="style-video-camera-video"
            ></video>
            <canvas ref="canvas" style="display: none;"></canvas>

            <!-- KHUNG DI CHUYỂN THEO KHUÔN MẶT -->
            <div
                ref="faceTracker"
                class="face-tracker-overlay"
                :class="{'detected': currentFaceBox }"
            >
              <div class="face-box">
                <div class="face-glow"></div>
              </div>
            </div>
          </div>

          <div class="box-status-camera">
            <TextInvalid :text-span="statusCamera" :is-view="statusError"/>
            <TextSuccess :text-span="statusCamera" :is-view="statusSuccess"/>
          </div>
          <nav class="nav-btn-control-take-photo">
            <ButtonBlue :disable-button="buttonTakeScreenShot.btnDisable"
                        :loading-button="buttonTakeScreenShot.btnLoading"
                        :text-button="buttonTakeScreenShot.btnText"
                        class="button-control"
                        @click="checkTextButtonToToggle"
            />
            <ButtonBlue :disable-button="buttonResetData.btnDisable"
                        :loading-button="buttonResetData.btnLoading"
                        :text-button="buttonResetData.btnText"
                        class="button-control"
            />
          </nav>
        </div>
        <div class="box-view-employee">
          <h5>Detail Employee</h5>
          <div class="box-view-image-employee">
            <img src="@/assets/images/img-employee-face/quang-nhat.jpg"
                 alt="image face employee"
                 class="img-employee-face"
            >
          </div>
          <div class="box-view-text-employee">
            <span class="span-txt-employee">Employee ID: {{ employee.employeeID }}</span>
            <span class="span-txt-employee">Employee Name: {{ employee.employeeName }}</span>
            <span class="span-txt-employee">Gender: {{ getGenderFromBoolean(employee.gender) }}</span>
            <span class="span-txt-employee">Position: {{ employee.position }}</span>
          </div>
        </div>
      </div>
    </main>
  </section>

</template>

<style scoped lang="scss">
.button-control {
  width: 20rem;
  height: 3.5rem;
}
</style>