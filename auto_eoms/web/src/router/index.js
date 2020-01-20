import Vue from 'vue';
import Router from 'vue-router';
import Builds from '../components/page/BuildsTable'
import Tests from '../components/page/TestsTable'
import Process from '../components/page/ProcessTable'
import Hardware from '../components/page/HardwareTable'
import Software from '../components/page/SoftwareTable'

Vue.use(Router);

export default new Router({
    // mode: 'history',
    routes: [
        {
            path: '/',
            redirect: '/commits'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: {title: '自述文件'},
            children: [
                {
                    path: '/commits',
                    component: () => import ('../components/page/CommitsTable.vue'),
                    meta: {title: '基础表格'}
                },
                {
                    path: '/404',
                    component: () => import('../components/page/404.vue'),
                    meta: {title: '404'}
                },
                {
                    path: '/builds',
                    name: 'Builds',
                    component: Builds
                },
                {
                    path: '/tests',
                    name: 'Tests',
                    component: Tests
                },
                {
                    path: '/process',
                    name: 'Process',
                    component: Process
                },
                {
                    path: '/hardware',
                    name: 'Hardware',
                    component: Hardware
                },
                {
                    path: '/software',
                    name: 'Software',
                    component: Software
                },
                {
                    path: 'mapa_market_download',
                    component: () => import ('../components/page/MapaMarketDownload.vue'),
                    meta: {title: 'mapa下载'}
                },
                {
                    path: 'android_phone_market_download',
                    component: () => import ('../components/page/AndroidPhoneMarketDownload.vue'),
                    meta: {title: 'app下载'}
                },
                {
                    path: 'help',
                    component: () => import ('../components/page/Help.vue'),
                    meta: {title: '帮助'}
                },
                {
                    path: 'models_and_networks',
                    component: () => import ('../components/page/ModelsAndNetworks.vue'),
                    meta: {title: '模型和网络'}
                },
                {
                    path: 'android_phone_package_manager_auto_build',
                    component: () => import ('../components/page/AndroidPhonePackageManagerAutoBuild.vue'),
                    meta: {title: 'android phone 自动触发的build信息'}
                },
                {
                    path: 'android_phone_package_manager_manual_build',
                    component: () => import ('../components/page/AndroidPhonePackageManagerManualBuild.vue'),
                    meta: {title: 'android phone 自动触发的build信息'}
                },
                {
                    path: 'mapa_package_manager_auto_build',
                    component: () => import ('../components/page/MapaPackageManagerAutoBuild.vue'),
                    meta: {title: 'android phone 自动触发的build信息'}
                },
                {
                    path: 'mapa_package_manager_manual_build',
                    component: () => import ('../components/page/MapaPackageManagerManualBuild.vue'),
                    meta: {title: 'android phone 自动触发的build信息'}
                },
            ]
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
