<template>
  <md-layout class="email" md-row md-align="center" md-vertical-align="center" md-gutter>
    <md-input-container class="email-input-container" md-clearable md-inline>
      <md-input
        :placeholder="$t('email.input.placeholder')"
        v-model="email" @input="onEmailChanged"/>
    </md-input-container>
  </md-layout>
</template>

<script>
import Vue from 'vue';

import store from '../reducers/Store';

export default Vue.component('email', {
  data() {
    return {
      email: this.$select('email'),  // Saved in redux store.
    };
  },
  methods: {
    onEmailChanged(value) {
      store.dispatch(store.actions.setEmail(value));
    },
  },
});
</script>

<style scoped>
.email-input-container {
  width: 300px;
}
</style>
