import '@babel/polyfill';
// Import Component hooks before component definitions
import './component-hooks';
import Vue from 'vue';
import './plugins/vuetify';
import './plugins/vee-validate';
import App from './App.vue';
import router from './router';
import store from '@/store';
import './registerServiceWorker';
import 'vuetify/dist/vuetify.min.css';
import HighchartsVue from 'highcharts-vue';
import Highcharts from 'highcharts';
import highchartsMore from 'highcharts/highcharts-more';
import stockInit from 'highcharts/modules/stock';

highchartsMore(Highcharts);
stockInit(Highcharts);
Vue.use(HighchartsVue);

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
