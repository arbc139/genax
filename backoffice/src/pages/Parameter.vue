<template>
  <md-layout md-column md-align="start">
    <md-input-container
      :class="{
        'input-container': true,
        'md-input-invalid': !conditions.MIN_SUP,
      }"
    >
      <label>{{ $t('parameter.labels.MIN_SUP') }}</label>
      <md-input v-model="parameters.MIN_SUP" type="number" />
      <span class="md-error" v-show="!conditions.MIN_SUP">
        {{ $t('parameter.errorMessages.MIN_SUP') }}
      </span>
    </md-input-container>
    <md-input-container
      :class="{
        'input-container': true,
        'md-input-invalid': !conditions.MAX_PVAL,
      }"
    >
      <label>{{ $t('parameter.labels.MAX_PVAL') }}</label>
      <md-input v-model="parameters.MAX_PVAL" type="number" />
      <span class="md-error" v-show="!conditions.MAX_PVAL">
        {{ $t('parameter.errorMessages.MAX_PVAL') }}
      </span>
    </md-input-container>
    <md-input-container
      :class="{
        'input-container': true,
        'md-input-invalid': !conditions.COOC_EM,
      }"
    >
      <label>{{ $t('parameter.labels.COOC_EM') }}</label>
      <md-select
        name="parameter-COOCEM"
        id="parameter-COOCEM"
        v-model="parameters.COOC_EM"
      >
        <md-option :value="0">{{ $t('parameter.selects.COOC_EM.support') }}</md-option>
        <md-option :value="1">{{ $t('parameter.selects.COOC_EM.logPvalue') }}</md-option>
        <md-option :value="2">{{ $t('parameter.selects.COOC_EM.oddRatio') }}</md-option>
        <md-option :value="3">{{ $t('parameter.selects.COOC_EM.relativeRisk') }}</md-option>
        <md-option :value="4">{{ $t('parameter.selects.COOC_EM.lift') }}</md-option>
        <md-option :value="5">{{ $t('parameter.selects.COOC_EM.chiSquaredStatistic') }}</md-option>
        <md-option :value="6">{{ $t('parameter.selects.COOC_EM.phiCoefficient') }}</md-option>
        <md-option :value="7">{{ $t('parameter.selects.COOC_EM.contingencyCoefficient') }}</md-option>
      </md-select>
      <span class="md-error" v-show="!conditions.COOC_EM">
        {{ $t('parameter.errorMessages.COOC_EM') }}
      </span>
    </md-input-container>
  </md-layout>
</template>

<script>
import Vue from 'vue';

import store from '../reducers/Store';

export default Vue.component('parameter', {
  props: ['conditions'],
  data() {
    return {
      parameters: this.$select('parameters'),
    };
  },
  watch: {
    parameters: {
      handler(newParameter) {
        store.dispatch(store.actions.setParameters(newParameter));
      },
      deep: true,
    },
  },
});
</script>

<style scoped>
.input-container {
  width: 50%;
}

.parameters-label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.54);
}
</style>
