<template>
  <md-whiteframe md-elevation="2">
    <md-layout class="result-parameter" md-column md-align="start">
      <md-whiteframe class="result-parameter-search-options" md-elevation="2">
        <md-layout
          md-column
          md-align="start"
        >
          <md-toolbar class="md-dense">
            <h2 class="md-theme-default md-subheading result-parameter-option-title">Search Options</h2>
          </md-toolbar>
          <div class="result-parameter-options">
            <md-input-container
              v-for="option in searchOptions"
              :key="option.id"
            >
              <label>{{ option.label }}</label>
              <md-input v-model="option.content" readonly />
            </md-input-container>
          </div>
        </md-layout>
      </md-whiteframe>
      <md-whiteframe class="result-parameter-cooccurence-options" md-elevation="2">
        <md-layout
          md-column
          md-align="start"
        >
          <md-toolbar class="md-dense">
            <h2 class="md-subheading result-parameter-option-title">Co-occurence Mining Options</h2>
            <md-button
              class="md-icon-button"
              v-show="isCoOccurenceOptionsExpanded"
              @click="closeCoOccurenceOptions()"
            >
              <md-icon>expand_less</md-icon>
            </md-button>
            <md-button
              class="md-icon-button"
              v-show="!isCoOccurenceOptionsExpanded"
              @click="openCoOccurenceOptions()"
            >
              <md-icon>expand_more</md-icon>
            </md-button>
          </md-toolbar>
          <div class="result-parameter-options" v-show="isCoOccurenceOptionsExpanded">
            <md-input-container
              v-for="option in coOccurenceOptions"
              :key="option.id"
            >
              <label>{{ option.label }}</label>
              <md-input v-model="option.content" readonly />
            </md-input-container>
          </div>
        </md-layout>
      </md-whiteframe>
    </md-layout>
  </md-whiteframe>
</template>

<script>
export default {
  props: ['searchOptions', 'coOccurenceOptions'],
  name: 'result-parameter',
  data() {
    return {
      isCoOccurenceOptionsExpanded: false,
    };
  },
  methods: {
    openCoOccurenceOptions() {
      this.isCoOccurenceOptionsExpanded = true;
    },
    closeCoOccurenceOptions() {
      this.isCoOccurenceOptionsExpanded = false;
    },
  },
};
</script>

<style scoped>
.result-parameter {
  padding: 16px;
}

.result-parameter-search-options {
  margin-bottom: 16px;
}

.result-parameter-cooccurence-options {
}

.result-parameter-option-title {
  flex: 1;
}

.result-parameter-options {
  padding: 16px;
}
</style>
