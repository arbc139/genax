<template>
  <md-layout
    class="query-condition"
    md-row
    md-align="center"
    md-vertical-align="center"
    md-gutter
  >
    <md-select
      class="type-selector"
      v-model="value.type"
      v-show="showSelector"
    >
      <md-option value="NOT">NOT</md-option>
      <md-option value="AND">AND</md-option>
      <md-option value="OR">OR</md-option>
    </md-select>
    <md-input-container class="condition-container" md-inline md-flex>
      <!--
        TODO(totoro): 'vue-material@0.7.5'에서 value.keyword가 사라지는 버그가 있음.
        사라지지 않도록 workaround를 찾아야함.
      -->
      <md-autocomplete
        :placeholder="$t('query.condition.input.placeholder')"
        v-model="value.keyword"
        :fetch="fetchDiseases"
        :prepare-response-data="formatDiseases"
        :debounce="200"
        print-attribute="name"
        ref="input"
        @keyup.enter.native="onEnterClicked"
      />
    </md-input-container>
    <md-button class="md-icon-button md-raised md-dense" @click="onButtonClicked">
      <md-icon>{{ conditionMode === 'CONDITION_MODE_ADD' ? 'add' : 'remove' }}</md-icon>
    </md-button>
  </md-layout>
</template>

<script>
import Vue from 'vue';
import _ from 'lodash';
import { ConditionMode } from '../structures/QueryConditionObject';

export default Vue.component('query-condition', {
  props: {
    conditionMode: {
      type: String,
      required: true,
    },
    value: {
      type: Object,
      required: true,
    },
    showSelector: {
      type: Boolean,
    },
  },
  watch: {
    value: {
      handler() {
        this.$emit('updated');
      },
      deep: true,
    },
  },
  mounted() {
    setTimeout(() => {
      const inputElement = _.get(this.$refs, 'input.$el.children[0].children[0]');
      inputElement.focus();
    }, 20);
  },
  methods: {
    onButtonClicked() {
      if (this.conditionMode === ConditionMode.add) {
        this.$emit('add');
      } else {
        this.$emit('remove');
      }
    },
    onEnterClicked() {
      if (this.conditionMode === 'CONDITION_MODE_ADD') {
        this.onButtonClicked();
      }
    },
    fetchDiseases(param) {
      return this.$http.get(`diseases/${param.q}`);
    },
    formatDiseases(response) {
      const diseases = response.data;
      return _.map(diseases, disease => ({
        id: disease.DIS_ID,
        name: disease.DIS_NAME,
      }));
    },
  },
});
</script>

<style scoped>
.query-condition {
  width: 100%;
}

.type-selector {
  width: 100px;
  min-width: auto;
}

.condition-container {
  width: auto;
  flex: 1;
}
</style>
