<template>
    <div class="sidebar">
        <el-menu
                class="sidebar-el-menu"
                :default-active="onRoutes"
                :collapse="collapse"
                background-color="#324157"
                text-color="#bfcbd9"
                active-text-color="#20a0ff"
                unique-opened
                router
        >
            <template v-for="item in items">
                <template v-if="item.subs">
                    <el-submenu :index="item.index" :key="item.index">
                        <template slot="title">
                            <i :class="item.icon"></i>
                            <span slot="title">{{ item.title }}</span>
                        </template>
                        <template v-for="subItem in item.subs">
                            <el-submenu
                                    v-if="subItem.subs"
                                    :index="subItem.index"
                                    :key="subItem.index"
                            >
                                <template slot="title">{{ subItem.title }}</template>
                                <el-menu-item
                                        v-for="(threeItem,i) in subItem.subs"
                                        :key="i"
                                        :index="threeItem.index"
                                >{{ threeItem.title }}
                                </el-menu-item>
                            </el-submenu>
                            <el-menu-item
                                    v-else
                                    :index="subItem.index"
                                    :key="subItem.index"
                            >{{ subItem.title }}
                            </el-menu-item>
                        </template>
                    </el-submenu>
                </template>
                <template v-else>
                    <el-menu-item :index="item.index" :key="item.index">
                        <i :class="item.icon"></i>
                        <span slot="title">{{ item.title }}</span>
                    </el-menu-item>
                </template>
            </template>
        </el-menu>
    </div>
</template>
<script>
    import bus from '../common/bus';

    export default {
        data() {
            return {
                collapse: false,
                items: [
                    {
                        icon: 'el-icon-lx-cascades',
                        index: 'commits',
                        title: '整机测试报告'
                    },
                    {
                        icon: 'el-icon-download',
                        index: '1',
                        title: '下载包管理',
                        subs: [
                            {
                                index: 'android_phone_package_manager_auto_build',
                                title: 'AndroidPhone自动Build',
                            },
                            {
                                index: 'android_phone_package_manager_manual_build',
                                title: 'AndroidPhone手动Build',
                            },
                            {
                                index: 'mapa_package_manager_auto_build',
                                title: 'Mapa自动Build',
                            },
                            {
                                index: 'mapa_package_manager_manual_build',
                                title: 'Mapa手动Build',
                            },

                            {
                                index: 'mapa_market_download',
                                title: 'MAPA市场部下载',
                            },
                            {
                                index: 'android_phone_market_download',
                                title: 'AndroidPhone市场部下载',
                            }
                        ]
                    },
                    {
                        icon: 'el-icon-video-camera-solid',
                        index: '2',
                        title: '算法管理',
                        subs: [
                            {
                                index: 'models_and_networks',
                                title: '模型和网络',
                            },
                        ]
                    },
                    {
                        icon: 'el-icon-help',
                        index: 'help',
                        title: '帮助',
                    }
                ]
            }
        },
        computed: {
            onRoutes() {
                return this.$route.path.replace('/commits', '');
            }
        },
        created() {
            // 通过 Event Bus 进行组件间通信，来折叠侧边栏
            bus.$on('collapse', msg => {
                this.collapse = msg;
            })
        }
    }
</script>

<style scoped>
    .sidebar {
        display: block;
        position: absolute;
        left: 0;
        top: 70px;
        bottom: 0;
        overflow-y: scroll;
    }

    .sidebar::-webkit-scrollbar {
        width: 0;
    }

    .sidebar-el-menu:not(.el-menu--collapse) {
        width: 250px;
    }

    .sidebar > ul {
        height: 100%;
    }
</style>
