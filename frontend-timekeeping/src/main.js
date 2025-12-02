// import './assets/main.css'
import './assets/main.scss'

import { createApp } from 'vue'
import App from './App.vue'
//import bootstrap
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';

//import vue routers
import { createRouter, createWebHistory } from 'vue-router';
import routers from "@/routers/routers.js";
//import vuetify
//vuetify
//npm install vuetify@next @mdi/font
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import 'vuetify/dist/vuetify-labs.min.css';
const vuetify = createVuetify();
import CanvasJSChart from '@canvasjs/vue-charts';
const app = createApp(App);
app.use(CanvasJSChart);
app.use(vuetify);

function initPage(routers, routerPath) {
    const router = createRouter({
        // mode: 'history',
        history: createWebHistory(),
        routes: routers,
    });
    app.use(router);
    router.replace(routerPath).catch((error) => {
        console.error('Error navigating: ', error);
        //router.replace('/screen-404').catch(err => console.error(err));
    });
    //app.unmount();
    //app.use(Vue3GeoLocation);
    app.mount('#app')
}

const routerPathInit = '/timekeeping-camera';
const pathExists = routers.some(router => router.path === routerPathInit);
if (pathExists && routers.length > 0) {
    const currentPath = window.location.pathname;
    let currentPathExists = routers.some(router => router.path === currentPath.trim());

    if (currentPathExists) {
        let currentPathTrim = currentPath.trim();
        initPage(routers, currentPathTrim);
    } else {
        initPage(routers, '/page-not-found');
        // Initialize to 404 path
    }
} else {
    initPage(routers, '/timekeeping-camera');
}
// createApp(App).mount('#app')
