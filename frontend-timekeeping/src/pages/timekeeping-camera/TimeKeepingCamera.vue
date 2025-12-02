<script>
import AsideMenu from "@/components/aside/aside-menu/AsideMenu.vue";
import './timekeeping-camera.scss';
import RouterManagement from "@/routers/RouterManagement.js";
export default {
  name: "TimeKeepingCamera",

  components: {
    AsideMenu,
  },

  data() {

  },

  props: {

  },

  created() {
    this.saveRouterPath(this.getRoute());
    this.setTitlePage();
  },

  mounted(){

  },

  methods: {
    setTitlePage() {
      document.title = 'Chụp ảnh chấm công';
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

    </main>
  </section>

</template>

<style scoped lang="scss">

</style>