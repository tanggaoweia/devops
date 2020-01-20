import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import ElementUI from 'element-ui';
import VueI18n from 'vue-i18n';
import { messages } from './components/common/i18n';
import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import '../static/css/theme-green/index.css';       // 浅绿色主题
import './assets/css/icon.css';
import './components/common/directives';
import "babel-polyfill";

// axios.defaults.baseURL =  'http://10.1.1.76:8888/v1';  // 76
axios.defaults.baseURL =  'http://10.1.1.18:8888/v1';  // 18
// axios.defaults.baseURL =  'http://127.0.0.1:8000';  //本地服务器
// axios.defaults.baseURL = 'http://10.1.1.111:8888';  // 111服务器 容器IP
global.axios = axios;  //设置一个全局axios便于调用

Vue.config.productionTip = false;

Vue.use(VueI18n);
Vue.use(ElementUI, {
    size: 'small'
});
Vue.prototype.$axios = axios;

const i18n = new VueI18n({
    locale: 'zh',
    messages
});

new Vue({
    router,
    i18n,
    render: h => h(App)
}).$mount('#app');
