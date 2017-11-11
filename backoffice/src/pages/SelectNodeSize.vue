<template>
  <md-layout md-column>
    <md-input-container
      :class="{
        'input-container': true,
        'md-input-invalid': !conditions.metricScore,
      }"
    >
      <label>{{ $t('selectNodeSize.metricScore.label') }}</label>
      <md-input v-model="metricScore" />
      <span class="md-error" v-show="!conditions.metricScore">
        {{ $t('selectNodeSize.metricScore.errorMessage') }}
      </span>
    </md-input-container>
    <md-input-container
      :class="{
        'input-container': true,
        'md-input-invalid': !conditions.nodeSize,
      }"
    >
      <label>{{ $t('selectNodeSize.nodeSize.label') }}</label>
      <md-input v-model="nodeSize" />
      <span class="md-error" v-show="!conditions.nodeSize">
        {{ $t('selectNodeSize.nodeSize.errorMessage') }}
      </span>
    </md-input-container>
  </md-layout>
</template>

<script>
import Vue from 'vue';

import store from '../reducers/Store';

export default Vue.component('select-node-size', {
  props: ['conditions'],
  data() {
    return {
      nodeSize: this.$select('nodeSize'),
      metricScore: this.$select('metricScore'),
    };
  },
  watch: {
    nodeSize(newValue) {
      store.dispatch(store.actions.setNodeSize(newValue));
    },
    metricScore(newValue) {
      store.dispatch(store.actions.setMetricScore(newValue));
    },
  },
});
</script>

<style scoped>
.input-container {
  width: 50%;
}
</style>
