import Vue from 'vue';
import Router from 'vue-router';

import Main from '@/pages/Main';

import About from '@/pages/main-tabs/About';
import MainTabs from '@/pages/main-tabs/MainTabs';
import Stepper from '@/pages/stepper/Stepper';
import Performance from '@/pages/main-tabs/Performance';

import Result from '@/pages/result/Result';
import ResultTable from '@/pages/result/ResultTable';
import ResultReference from '@/pages/result/ResultReference';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      component: Main,
      children: [
        {
          path: '',
          component: MainTabs,
          redirect: 'about',
          children: [
            {
              path: 'about',
              name: 'About',
              component: About,
            },
            {
              path: 'stepper',
              name: 'Stepper',
              component: Stepper,
            },
            {
              path: 'performance',
              name: 'Performance',
              component: Performance,
            },
          ],
        },
        {
          path: 'result/:jobKey',
          component: Result,
          children: [
            {
              path: '',
              name: 'Result',
              component: ResultTable,
            },
            {
              path: 'references/:hgncId',
              name: 'References',
              component: ResultReference,
              props: true,
            },
          ],
        },
      ],
    },
  ],
});
