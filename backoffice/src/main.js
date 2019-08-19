// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import VueI18n from 'vue-i18n';
import VueMaterial from 'vue-material';
import VueResource from 'vue-resource';

import App from './App';
import router from './router';

import translationEN from './translations.en';
import translationKO from './translations.ko';

import backend from './configs/backend';

Vue.use(VueI18n);
Vue.use(VueMaterial);
Vue.use(VueResource);
Vue.config.productionTip = false;

Vue.material.registerTheme('default', {
  primary: {
    color: 'indigo',
    hue: '900',
    textColor: 'white',
  },
  accent: {
    color: 'pink',
    hue: '500',
    textColor: 'white',
  },  // 얘는 pink 그대로가 자연스러울 것 같음.
  warn: 'deep-orange',  // 얘는 deep-orange 그대로가 자연스러울 것 같음.
});

const i18n = new VueI18n({
  locale: 'en',
  messages: {
    en: translationEN,
    ko: translationKO,
  },
});

Vue.http.options.root = `http://${backend.ip}:${backend.port}`;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
  i18n,
});
