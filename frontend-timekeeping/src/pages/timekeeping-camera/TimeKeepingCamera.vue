<script>
import AsideMenu from "@/components/aside/aside-menu/AsideMenu.vue";
import './timekeeping-camera.scss';
import RouterManagement from "@/routers/RouterManagement.js";
import ButtonBlue from "@/components/button/button-blue/ButtonBlue.vue";
import TextInvalid from "@/components/span/TextInvalid.vue";
import TransformText from "@/others/TransformText.js";
import TextSuccess from "@/components/span/TextSuccess.vue";
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
      currentStream: null,
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

  onUnmounted() {
    this.closeCameraComputer();
  },

  methods: {
    setTitlePage() {
      document.title = 'Take a photo to check attendance';
    },

    async openCameraComputer() {
      navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            this.$refs.video.srcObject = stream;
            this.currentStream = stream;
            this.buttonTakeScreenShot.btnText = "Close camera";
          })
          .catch(err => {
            console.error(err);
          });
    },

    async closeCameraComputer() {
      if (this.currentStream) {
        const tracks = this.currentStream.getTracks();
        tracks.forEach(track => track.stop()); // Dừng tất cả các track
        this.$refs.video.srcObject = null; // Đặt srcObject về null
        this.currentStream = null; // Xóa stream đã lưu
        this.buttonTakeScreenShot.btnText = "Open camera";
      }
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

    async startOpenCamera() {

      try {
        //liên kết camera
        await this.openCameraComputer();


        // Bắt đầu vòng lặp detect
        // detectInterval = setInterval(detectFaces, 100) // 300ms là ổn, nhẹ
      } catch (err) {
       // error.value = 'Không mở được camera: ' + err.message
        alert(err);
      }
    },

    async stopCamera() {

      try {
        //liên kết camera
        await this.closeCameraComputer();

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
<!--            <TextInvalid  text-span="An error occurred when open camera."/>-->
            <TextSuccess text-span="Detected face"/>
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