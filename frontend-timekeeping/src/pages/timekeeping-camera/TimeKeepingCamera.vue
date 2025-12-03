<script>
import AsideMenu from "@/components/aside/aside-menu/AsideMenu.vue";
import './timekeeping-camera.scss';
import RouterManagement from "@/routers/RouterManagement.js";
import ButtonBlue from "@/components/button/button-blue/ButtonBlue.vue";
export default {
  name: "TimeKeepingCamera",

  components: {
    ButtonBlue,
    AsideMenu,
  },

  data() {
    return {
      buttonTakeScreenShot : {
        btnDisable: false,
        btnText: "Take a photo",
        btnLoading: false,
      },
    }
  },

  props: {

  },

  created() {
    this.saveRouterPath(this.getRoute());
    this.setTitlePage();
  },

  mounted(){
    this.setCameraComputer();
  },

  methods: {
    setTitlePage() {
      document.title = 'Take a photo to check attendance';
    },

    setCameraComputer() {
      navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            this.$refs.video.srcObject = stream;
          });
    },

    getRoute() {
      //ở đây có props thì phải thêm path của props
      return this.$route.path;
    },

    saveRouterPath(route) {
      const routerManagement = new RouterManagement();
      routerManagement.savePathToSessionStorage(route);
    },
  },

  setup() {

  }
}
</script>

<template>
  <section class="section-time-keeping-camera">
    <AsideMenu/>
    <main class="main-time-keeping-camera">
      <div class="box-camera-and-employee">
        <div class="box-camera-take-photo">
          <video ref="video" autoplay class="style-video-camera"/>
          <ButtonBlue :disable-button="buttonTakeScreenShot.btnDisable"
                      :loading-button="buttonTakeScreenShot.btnLoading"
                      :text-button="buttonTakeScreenShot.btnText"
                      class="button-take-photo"
          />
        </div>
        <div class="box-view-employee">
          <h5>Detail Employee</h5>
          <div class="box-view-image-employee">
            <img src="@/assets/images/img-employee-face/quang-nhat.jpg" alt="image face employee"
                 class="img-employee-face"
                 >
          </div>
          <div class="box-view-text-employee">
            <span class="span-txt-employee">Employee ID: 1000</span>
            <span class="span-txt-employee">Employee Name: Tu Quang Nhat</span>
            <span class="span-txt-employee">Gender: Male</span>
            <span class="span-txt-employee">Position: Dev</span>
          </div>
        </div>
      </div>
    </main>
  </section>

</template>

<style scoped lang="scss">
.button-take-photo {
  width: 20rem;
  height: 3.5rem;
}
</style>