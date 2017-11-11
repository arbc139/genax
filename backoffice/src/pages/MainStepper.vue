<template>
  <!-- TODO(totoro): md-vertical option을 넣으면 layout이 깨지는 문제가 있음. -->
  <md-stepper
    class="main-stepper"
    md-alternate-labels
    @change="onStepChanged"
    @completed="onSubmitted"
  >
    <md-step
      :md-error="!enablePassQuery.condition"
      :md-continue="enablePassQuery.condition"
      :md-message="enablePassQuery.message"
    >
      <help-frame>
        <query-builder slot="tool" />
        <!-- TODO(totoro): Help component를 구현해야함. -->
        <help
          slot="help"
          :title="$t('query.help.title')"
          :instructions="$t('query.help.instructions')"
        />
      </help-frame>
    </md-step>
    <md-step
      :md-error="!enablePassPeriod.condition"
      :md-continue="enablePassPeriod.condition"
      :md-message="enablePassPeriod.message"
      :md-disabled="!enablePassQuery.condition"
    >
      <help-frame>
        <period slot="tool" />
        <help
          slot="help"
          :title="$t('period.help.title')"
          :instructions="$t('period.help.instructions')"
        />
      </help-frame>
    </md-step>
    <md-step
      :md-error="!enablePassParameter.condition"
      :md-continue="enablePassParameter.condition"
      :md-message="enablePassParameter.message"
      :md-disabled="!enablePassQuery.condition || !enablePassPeriod.condition"
    >
      <help-frame>
        <parameter slot="tool" :conditions="enablePassParameter.conditions" />
        <help
          slot="help"
          :title="$t('parameter.help.title')"
          :instructions="$t('parameter.help.instructions')"
        />
      </help-frame>
    </md-step>
    <md-step
      :md-error="!enablePassSelectNodeSize.condition"
      :md-continue="enablePassSelectNodeSize.condition"
      :md-message="enablePassSelectNodeSize.message"
      :md-disabled="
        !enablePassQuery.condition || !enablePassPeriod.condition ||
        !enablePassParameter.condition
      "
    >
      <help-frame>
        <select-node-size
          slot="tool"
          :conditions="enablePassSelectNodeSize.conditions"
        />
        <help
          slot="help"
          :title="$t('selectNodeSize.help.title')"
          :instructions="$t('selectNodeSize.help.instructions')"
        />
      </help-frame>
    </md-step>
    <md-step
      :md-disabled="
        !enablePassQuery.condition || !enablePassPeriod.condition ||
        !enablePassParameter.condition || !enablePassSelectNodeSize.condition
      "
    >
      <help-frame>
        <email slot="tool" />
        <help
          slot="help"
          :title="$t('email.help.title')"
          :instructions="$t('email.help.instructions')"
        />
      </help-frame>
    </md-step>
    <md-step
      :md-error="!enableSubmit.condition"
      :md-continue="
        state === STEPPER_STATE.NONE && enableSubmit.condition
      "
      :md-message="enableSubmit.message"
      :md-disabled="
        !enablePassQuery.condition || !enablePassPeriod.condition ||
        !enablePassParameter.condition || !enablePassSelectNodeSize.condition
      "
    >
      <check-parameter
        :pmidCount="pmidCount"
        :enablePmidCount="enablePmidCount"
      />
    </md-step>
  </md-stepper>
</template>

<script>
import Vue from 'vue';
import _ from 'lodash';

import router from '../router';
import store from '../reducers/Store';

import HelpFrame from '../components/HelpFrame';
import Help from '../components/Help';
import QueryBuilder from './QueryBuilder';
import Period from './Period';
import Parameter from './Parameter';
import SelectNodeSize from './SelectNodeSize';
import Email from './Email';
import CheckParameter from './CheckParameter';

const STEPPER_STATE = {
  NONE: 'STEPPER_STATE_NONE',
  QUERY_PERIOD_MODIFIED: 'STEPPER_STATE_QUERY_PERIOD_MODIFIED',
  PMID_COUNT_LOADING: 'STEPPER_STATE_PMID_COUNT_LOADING',
};

export default Vue.component('main-stepper', {
  components: {
    QueryBuilder,
    Period,
    Parameter,
    SelectNodeSize,
    Email,
    HelpFrame,
    Help,
    CheckParameter,
  },
  data() {
    return {
      query: this.$select('query'),
      period: this.$select('period'),
      parameters: this.$select('parameters'),
      metricScore: this.$select('metricScore'),
      nodeSize: this.$select('nodeSize'),
      email: this.$select('email'),
      STEPPER_STATE,
      state: STEPPER_STATE.NONE,
      pmidCount: this.$select('pmidCount'),
    };
  },
  watch: {
    query() {
      this.state = STEPPER_STATE.QUERY_PERIOD_MODIFIED;
    },
    period: {
      handler() {
        this.state = STEPPER_STATE.QUERY_PERIOD_MODIFIED;
      },
      deep: true,
    },
  },
  computed: {
    enablePassQuery() {
      const condition = this.query.length !== 0;
      return {
        condition,
        message: condition ? '' : this.$t('mainStepper.query.errorMessage'),
      };
    },
    enablePassPeriod() {
      const condition = !_.isEmpty(this.period);
      return {
        condition,
        message: condition ? '' : this.$t('mainStepper.period.errorMessage'),
      };
    },
    numberizedParameters() {
      const parameters = {};
      _.forEach(this.parameters, (value, key) => {
        parameters[key] = Number(value);
      });
      return parameters;
    },
    enablePassParameter() {
      const parameters = this.numberizedParameters;
      const conditions = {
        MIN_SUP: parameters.MIN_SUP >= 0.00001 && parameters.MIN_SUP <= 1,
        MAX_PVAL: parameters.MAX_PVAL >= 0.000001 && parameters.MAX_PVAL <= 1,
        COOC_EM: parameters.COOC_EM >= 0 && parameters.COOC_EM <= 7,
      };
      const condition = _.every(conditions);
      return {
        condition,
        conditions,
        message: condition ? '' : this.$t('mainStepper.parameter.errorMessage'),
      };
    },
    enablePassSelectNodeSize() {
      const conditions = {
        nodeSize: this.nodeSize > 0 && this.nodeSize <= 100,
        metricScore: this.metricScore >= 0.000001 && this.metricScore <= 1,
      };
      const condition = _.every(conditions);
      return {
        condition,
        conditions,
        message: condition ? '' : this.$t('mainStepper.selectNodeSize.errorMessage'),
      };
    },
    enablePmidCount() {
      const condition = this.pmidCount <= 5000000;
      return {
        condition,
        message: this.$t('mainStepper.pmidCount.errorMessage'),
      };
    },
    enableSubmit() {
      const condition = this.enablePassQuery.condition &&
        this.enablePassPeriod.condition && this.enablePassParameter.condition &&
        this.enablePassSelectNodeSize.condition &&
        this.enablePmidCount.condition;
      return {
        condition,
        message: condition ? '' : this.$t('mainStepper.submit.errorMessage'),
      };
    },
  },
  methods: {
    onStepChanged(stepNumber) {
      if (stepNumber < 2 || this.state === STEPPER_STATE.NONE) {
        return;
      }
      this.state = STEPPER_STATE.PMID_COUNT_LOADING;
      this.$http.get('pmid_counts', {
        params: {
          searchQuery: this.query,
          startDate: this.period.start.format('YYYY/MM/DD'),
          endDate: this.period.end.format('YYYY/MM/DD'),
        },
      }).then((response) => {
        this.state = STEPPER_STATE.NONE;
        const pmidCount = _.get(response.body, 'pmidCount[0]');
        store.dispatch(store.actions.setPmidCount(pmidCount));
      }, () => {
        this.state = STEPPER_STATE.NONE;
      });
    },
    onSubmitted() {
      this.$http.post(
        'job_insert',
        _.defaults({
          query: this.query,
          start_date: this.period.start.format('YYYY/MM/DD'),
          end_date: this.period.end.format('YYYY/MM/DD'),
          MIN_NODE_SUP: this.metricScore,
          node_size: this.nodeSize,
          email: this.email,
        }, this.parameters))
        .then((response) => {
          const { insertId } = response.body;
          return this.$http.get(`id2keys/${insertId}`);
        })
        .then((response) => {
          const jobKey = _.get(response.body, '[0].J_KEY');
          router.push({
            name: 'Result',
            params: { jobKey },
          });
        });
    },
  },
});
</script>

<style>
.main-stepper {
  overflow: hidden;
}

/* Workaround for scrolling without step navigator. */
.main-stepper .md-steps-navigation-container {
  margin-bottom: 0 !important;
}

/* Workaround for scrolling without step navigator. */
.main-stepper :not(.md-steps-navigation).md-whiteframe.md-whiteframe-1dp {
  overflow: auto;
  -webkit-box-shadow: none;
  box-shadow: none;
}
</style>
