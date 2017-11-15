import Vue from 'vue';
import Router from 'vue-router';

import About from '@/pages/main-tabs/About';
import Result from '@/pages/Result';
import Main from '@/pages/Main';
import MainTabs from '@/pages/main-tabs/MainTabs';
import Performance from '@/pages/main-tabs/Performance';
import Stepper from '@/pages/Stepper';

import ResultTable from '@/components/ResultTable';
import ResultReference from '@/components/ResultReference';

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
