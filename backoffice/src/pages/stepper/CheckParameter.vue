<template>
  <md-layout md-column>
    <md-input-container class="input-container">
      <label>{{ $t('checkParameter.labels.query') }}</label>
      <md-input v-show="!!query" v-model="query" readonly />
    </md-input-container>
    <md-input-container class="input-container">
      <label>{{ $t('checkParameter.labels.period') }}</label>
      <md-input v-show="!!displayPeriod" v-model="displayPeriod" readonly />
    </md-input-container>
    <md-input-container
      class="input-container"
      v-for="parameter in displayParameters"
      :key="parameter.key"
    >
      <label>
        {{ $t(`checkParameter.labels.parameters.${parameter.key}`) }}
      </label>
      <md-input v-show="!!parameter.value" v-model="parameter.value" readonly />
    </md-input-container>
    <md-input-container class="input-container">
      <label>{{ $t('checkParameter.labels.metricScore') }}</label>
      <md-input v-show="!!metricScore" v-model="metricScore" readonly />
    </md-input-container>
    <md-input-container class="input-container">
      <label>{{ $t('checkParameter.labels.nodeSize') }}</label>
      <md-input v-show="!!nodeSize" v-model="nodeSize" readonly />
    </md-input-container>
    <md-input-container class="input-container">
      <label>{{ $t('checkParameter.labels.email') }}</label>
      <md-input v-show="!!email" v-model="email" readonly />
    </md-input-container>
    <md-input-container
      :class="{
        'input-container': true,
        'md-input-invalid': !enablePmidCount.condition,
      }"
    >
      <label>{{ $t('checkParameter.labels.pmidCount') }}</label>
      <md-input v-show="!!pmidCount" v-model="pmidCount" readonly />
      <span class="md-error" v-show="!enablePmidCount.condition">
        {{ enablePmidCount.message }}
      </span>
    </md-input-container>
  </md-layout>
</template>

<script>
import _ from 'lodash';

export default {
  props: ['pmidCount', 'enablePmidCount'],
  name: 'check-parameter',
  data() {
    return {
      query: this.$select('query'),
      period: this.$select('period'),
      parameters: this.$select('parameters'),
      metricScore: this.$select('metricScore'),
      nodeSize: this.$select('nodeSize'),
      email: this.$select('email'),
    };
  },
  computed: {
    displayPeriod() {
      return `${this.period.start.format('YYYY/MM/DD')} ~ ${this.period.end.format('YYYY/MM/DD')}`;
    },
    displayParameters() {
      const displayParameters = [];
      _.forEach(this.parameters, (value, key) => {
        const displayParameter = {
          key,
          value: String(value),
        };
        if (key === 'COOC_EM') {
          displayParameter.value = this.convertCoocEM(value);
        }
        displayParameters.push(displayParameter);
      });
      return displayParameters;
    },
  },
  methods: {
    convertCoocEM(coocEMValue) {
      switch (coocEMValue) {
        case 0:
          return this.$t('parameter.selects.COOC_EM.support');
        case 1:
          return this.$t('parameter.selects.COOC_EM.logPvalue');
        case 2:
          return this.$t('parameter.selects.COOC_EM.oddRatio');
        case 3:
          return this.$t('parameter.selects.COOC_EM.relativeRisk');
        case 4:
          return this.$t('parameter.selects.COOC_EM.lift');
        case 5:
          return this.$t('parameter.selects.COOC_EM.chiSquaredStatistic');
        case 6:
          return this.$t('parameter.selects.COOC_EM.phiCoefficient');
        case 7:
          return this.$t('parameter.selects.COOC_EM.contingencyCoefficient');
        default:
          return 'ERROR';
      }
    },
  },
};
</script>

<style scoped>
.input-container {
  width: 50%;
}
</style>
