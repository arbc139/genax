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
    <label class="radio-label">{{ $t('parameter.labels.COOC_EM') }}</label>
    <md-layout md-column md-align="start">
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-support"
        name="cooc-em-support"
        :md-value="0"
      >
        {{ $t('parameter.selects.COOC_EM.support') }}
      </md-radio>
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-logPvalue"
        name="cooc-em-logPvalue"
        :md-value="1"
      >
        {{ $t('parameter.selects.COOC_EM.logPvalue') }}
      </md-radio>
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-oddRatio"
        name="cooc-em-oddRatio"
        :md-value="2"
      >
        {{ $t('parameter.selects.COOC_EM.oddRatio') }}
      </md-radio>
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-lift"
        name="cooc-em-lift"
        :md-value="4"
      >
        {{ $t('parameter.selects.COOC_EM.lift') }}
      </md-radio>
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-chiSquaredStatistic"
        name="cooc-em-chiSquaredStatistic"
        :md-value="5"
      >
        {{ $t('parameter.selects.COOC_EM.chiSquaredStatistic') }}
      </md-radio>
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-phiCoefficient"
        name="cooc-em-phiCoefficient"
        :md-value="6"
      >
        {{ $t('parameter.selects.COOC_EM.phiCoefficient') }}
      </md-radio>
      <md-radio
        v-model="parameters.COOC_EM"
        id="cooc-em-contingencyCoefficient"
        name="cooc-em-contingencyCoefficient"
        :md-value="7"
      >
        {{ $t('parameter.selects.COOC_EM.contingencyCoefficient') }}
      </md-radio>
    </md-layout>
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

.radio-label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.54);
}
</style>
