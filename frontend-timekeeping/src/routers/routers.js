
import TimeKeepingCamera from "@/pages/TimeKeepingCamera.vue";
import ManageListEmployees from "@/pages/ManageListEmployees.vue";
import PageNotFound from "@/pages/PageNotFound.vue";


const routers = [
    // '/' khi init trang, prop param de truyen tham so.
    { path: '/', component: TimeKeepingCamera, allow: true},
    { path: '/timekeeping-camera', component: TimeKeepingCamera, allow: true},
    { path: '/manage-list-employees', component: ManageListEmployees, allow: true },
    { path: '/page-not-found', component: PageNotFound, allow: true },
];
export default routers;
/*
*
* props: (route) => ({ bankTestJavaOopID: route.query.bankTestJavaOopID })
*/