<script>
import './manage-list-employee.scss';
import AsideMenu from "@/components/aside/aside-menu/AsideMenu.vue";
import RouterManagement from "@/routers/RouterManagement.js";

export default {
  name: "ManageListEmployees",

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
      document.title = 'Danh sách nhân viên chấm công';
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
  <section class="section-list-employees">
    <AsideMenu/>
    <main class="main-list-employees">

    </main>
  </section>
</template>

<style scoped lang="scss">

</style>