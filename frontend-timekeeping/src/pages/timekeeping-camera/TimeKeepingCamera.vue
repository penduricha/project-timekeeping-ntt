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
      buttonTakeScreenShot : {
        btnDisable: false,
        btnText: "Open camera",
        btnLoading: false,
      },

      buttonResetData : {
        btnDisable: false,
        btnText: "Reset data",
        btnLoading: false,
      },

      employee: {
        employeeID : 1000,
        employeeName : 'Tu Quang Nhat',
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
    }
  },

  props: {

  },

  created() {
    //set path
    this.saveRouterPath(this.getRoute());
    this.setTitlePage();
  },

  mounted(){
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
      // navigator.mediaDevices.getUserMedia(
      //     // { width: 'auto', height: 449.5, facingMode: 'user' },
      //     // audio: false
      //     {
      //       video: { width: 720, height: 560, facingMode: 'user' },
      //       audio: false
      //     }).then(stream => {
      //       this.$refs.video.srcObject = stream;
      //       this.currentStream = stream;
      //       this.buttonTakeScreenShot.btnText = "Close camera";
      //     })
      //     .catch(err => {
      //       console.error(err);
      //     });
      try{
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { width: 720, height: 560, facingMode: 'user' },
          audio: false
        })

        this.$refs.video.srcObject = stream
        this.currentStream = stream
        await this.$refs.video.play();
        this.buttonTakeScreenShot.btnText = "Close camera";
      }catch(error) {
        alert(error.message);
      }
    },

    async closeCameraComputer() {
      if (this.currentStream) {
        const tracks = this.currentStream.getTracks();
        tracks.forEach(track => track.stop()); // Dừng tất cả các track
        this.$refs.video.srcObject = null; // Đặt srcObject về null
        this.currentStream = null; // Xóa stream đã lưu
        this.buttonTakeScreenShot.btnText = "Open camera";
        //reset status camera và text
        this.resetCameraParameters();
      }
    },

    resetCameraParameters() {
      this.statusCamera = '';
      this.statusSuccess = true;
      this.statusError = false;
      //this.video = null;
      this.currentStream = null;
      this.faceDetectedBefore = false;
      this.detectInterval = null;
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
      } else if (this.buttonTakeScreenShot.btnText === "Close camera"){
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
        console.log('Models loaded thành công!')
        this.statusCamera = 'Face detection system is ready.';
      }catch (err) {
        this.statusCamera = err.message;
        this.statusError = true;
        this.statusSuccess = false;
        console.error(err)
      }
    },

    async detectedFace() {
      try {
        const detections = await faceapi.detectAllFaces(
            this.$refs.video,
            new faceapi.TinyFaceDetectorOptions({
              inputSize: 320,     // Nhẹ hơn, nhanh hơn
              scoreThreshold: 0.5
            })
        )

        const hasFace = detections.length > 0;

        if (hasFace && !this.faceDetectedBefore) {
          // CHỈ LOG 1 LẦN KHI MỚI PHÁT HIỆN
          console.log('Đã phát hiện')
          this.statusCamera = 'Detected face.';
          this.statusError = false;
          this.statusSuccess = true;
          this.faceDetectedBefore = true;
        } else if (!hasFace && this.faceDetectedBefore) {
          // Khi khuôn mặt biến mất
          this.statusCamera = 'Can not find a face.';
          this.statusError = true;
          this.statusSuccess = false;
          this.faceDetectedBefore = false;
        }
      } catch (err) {
        console.error('Lỗi detect:', err)
      }
    },

    async startOpenCamera() {
      try {
        //liên kết camera
        await this.openCameraComputer();
        await this.loadModelsFaceDetected();
        // 1/10 giây
        this.detectInterval = setInterval(this.detectedFace, 100);
      } catch (err) {
       // error.value = 'Không mở được camera: ' + err.message
        alert(err);
      }
    },

    async stopCamera() {

      try {
        //liên kết camera
        await this.closeCameraComputer();
        this.statusCamera = '';
        // Bắt đầu vòng lặp detect
        // detectInterval = setInterval(detectFaces, 100) // 300ms là ổn, nhẹ
      } catch (err) {
        // error.value = 'Không mở được camera: ' + err.message
        alert(err);
      }
    },
  },

  setup() {

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
            <video ref="video"
                   muted playsinline autoplay
                   class="style-video-camera-video"
            />
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
            <span class="span-txt-employee">Employee ID: {{employee.employeeID}}</span>
            <span class="span-txt-employee">Employee Name: {{employee.employeeName}}</span>
            <span class="span-txt-employee">Gender: {{getGenderFromBoolean(employee.gender)}}</span>
            <span class="span-txt-employee">Position: {{employee.position}}</span>
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