import Vue from 'vue';
import Router from 'vue-router';

import Result from '@/pages/Result';
import Main from '@/pages/Main';
import MainStepper from '@/pages/MainStepper';

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
          name: 'Stepper',
          component: MainStepper,
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
