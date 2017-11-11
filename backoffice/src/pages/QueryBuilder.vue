<template>
  <md-layout class="query-builder" md-column md-align="center" md-vertical-align="center" md-gutter>
    <md-layout class="query-container" md-row md-align="center" md-gutter>
      <md-input-container class="query-input-container" md-inline md-clearable md-flex>
        <md-input readonly v-model="query" />
      </md-input-container>
    </md-layout>
    <md-layout
      class="condition-layout"
      md-row
      md-align="center"
      md-gutter
      :key="condition.id"
      v-for="(condition, index) in conditions"
    >
      <query-condition
        :condition-mode="
            index === conditions.length - 1 ?
            'CONDITION_MODE_ADD' : 'CONDITION_MODE_REMOVE'"
        :show-selector="index !== 0"
        v-model="conditions[index]"
        v-on:add="onAddClicked()"
        v-on:remove="onRemoveClicked(index)"
        v-on:updated="onUpdateConditions"
      />
    </md-layout>
  </md-layout>
</template>

<script>
import Vue from 'vue';

import _ from 'lodash';

import store from '../reducers/Store';

import queryCondition from '../components/QueryCondition';
import { Condition } from '../structures/QueryConditionObject';

function buildQuery(conditions) {
  const parsedConditions = _.chain(conditions)
    .filter(condition => !_.isEmpty(condition.keyword))
    .map((condition, index) => {
      if (index === 0) {
        return `${condition.keyword}`;
      }
      return _.concat(`${condition.type} ${condition.keyword}`, ')').join('');
    })
    .value();
  const prefix = _.times(parsedConditions.length - 1, () => '(').join('');
  return _.concat(
    prefix, parsedConditions.join(' ')).join('');
}

export default Vue.component('query-builder', {
  components: { queryCondition },
  data() {
    return {
      query: this.$select('query'),  // Saved in redux store.
      conditions: this.$select('conditions'),  // Saved in redux store.
    };
  },
  watch: {
    query(newQuery) {
      if (!_.isEmpty(newQuery)) {
        return;
      }
      store.dispatch(store.actions.clearQuery());
    },
  },
  methods: {
    onAddClicked() {
      const condition = new Condition('AND', '');
      store.dispatch(store.actions.addCondition(condition));
      const query = buildQuery(this.conditions);
      store.dispatch(store.actions.setQuery(query));
    },
    onRemoveClicked(index) {
      store.dispatch(store.actions.removeCondition(index));
      if (index === 0 && this.conditions.length !== 0) {
        store.dispatch(store.actions.dropTypeOfFirstCondition());
      }
      const query = buildQuery(this.conditions);
      store.dispatch(store.actions.setQuery(query));
    },
    onUpdateConditions() {
      const query = buildQuery(this.conditions);
      store.dispatch(store.actions.setQuery(query));
    },
  },
});
</script>

<style scoped>
.query-container {
  width: 100%;
}

.query-input-container {
  width: auto;
  flex: 1;
}

.condition-layout {
  width: 100%;
}
</style>
