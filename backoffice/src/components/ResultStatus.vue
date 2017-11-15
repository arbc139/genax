<template>
  <md-whiteframe class="result-status" md-elevation="2">
    <md-layout
      class="status-title-container"
      md-row
      md-align="center"
      md-vertical-align="center"
    >
      <md-layout md-row md-align="center" md-vertical-align="center" md-flex>
        <span class="md-body-2">{{ title }}</span>
      </md-layout>
      <md-layout md-row md-align="center" md-vertical-align="center" md-flex
        :style="{color: translatedStatus.color}"
      >
        <span class="md-body-2">{{ translatedStatus.text }}</span>
      </md-layout>
    </md-layout>
    <md-layout
      :class="{
        'status-count-input-container': true,
        'blur': status === ResultStatusType.yet,
      }"
      md-column
      md-align="start"
      md-vertical-align="start"
      md-flex
      v-show="!showSpinner"
    >
      <md-input-container
        v-for="instruction in instructions"
        :key="instruction.id"
      >
        <label>{{ instruction.label }}</label>
        <md-input v-model="instruction.count" readonly />
      </md-input-container>
    </md-layout>
    <md-layout
      md-align="center"
      md-vertical-align="center"
      v-show="showSpinner"
    >
      <md-spinner
        md-indeterminate
      />
    </md-layout>
  </md-whiteframe>
</template>

<script>
import Vue from 'vue';

import ResultStatusType from '../structures/ResultStatusType';

export default Vue.component('result-status', {
  props: ['title', 'status', 'instructions'],
  computed: {
    translatedStatus() {
      if (this.status === ResultStatusType.running) {
        return {
          color: '#E91E63',
          text: this.$t('result.status.type.running'),
        };
      }
      if (this.status === ResultStatusType.done) {
        return {
          color: '#1a237e',
          text: this.$t('result.status.type.done'),
        };
      }
      return {
        color: '#000000',
        text: this.$t('result.status.type.yet'),
      };
    },
    showSpinner() {
      return this.status === ResultStatusType.running;
    },
  },
});
</script>

<style scoped>
.result-status {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 16px;
}

.status-title-container {
  flex: 36px 0 0;
  margin-bottom: 16px;
}

.blur {
  filter: blur(2px);
}

.status-count-input-container {
  width: 100%;
  min-width: 300px;
}
</style>
