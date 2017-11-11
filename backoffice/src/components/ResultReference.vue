<template>
  <md-whiteframe md-elevation="2" class="result-reference">
    <md-layout
      md-column
      md-align="start"
      md-vertical-align="center"
    >

      <md-table-card class="result-reference-wrapper">
        <md-toolbar class="md-transparent">
          <h1 class="md-title">{{ translatedTitle }}</h1>
          <md-button class="md-raised" @click="onDownloadClicked">
            {{ $t('common.downloadButton') }}
          </md-button>
        </md-toolbar>

        <md-table>
          <md-table-header>
            <md-table-row>
              <md-table-head>Index</md-table-head>
              <md-table-head>PubMed ID</md-table-head>
              <md-table-head md-numeric>Title</md-table-head>
            </md-table-row>
          </md-table-header>

          <md-table-body>
            <md-table-row
              v-for="(row, index) in references" :key="row.pmid" :md-item="row"
            >
              <md-table-cell>{{ startIndex + index }}</md-table-cell>
              <md-table-cell>
                <a
                  target="_blank"
                  class="a-tag-hover"
                  :href="`https://www.ncbi.nlm.nih.gov/pubmed/?term=${row.pmid}`"
                >
                  {{ row.pmid }}
                </a>
              </md-table-cell>
              <md-table-cell md-numeric>{{ row.title }}</md-table-cell>
            </md-table-row>
          </md-table-body>
        </md-table>

        <md-table-pagination
          :md-size="computedPaginationOptions.size"
          :md-total="computedPaginationOptions.total"
          :md-page="computedPaginationOptions.page"
          :md-label="computedPaginationOptions.label_"
          :md-separator="computedPaginationOptions.separator_"
          :md-page-options="computedPaginationOptions.pageOptions_"
          @page="onPaginationPage" @size="onPaginationSize"
        />
      </md-table-card>
    </md-layout>
  </md-whiteframe>
</template>

<script>
import Vue from 'vue';
import _ from 'lodash';
import Papa from 'papaparse';

import Bus from './Bus';

import pullingConfig from '../configs/pulling';

export default Vue.component('result-references', {
  props: ['jobId', 'hgncId'],
  watch: {
    jobId(newJobId) {
      this.getReferences(
        newJobId,
        this.hgncId,
        this.startIndex,
        this.computedPaginationOptions.size,
      );
    },
    hgncId(newHgncId) {
      this.getReferences(
        this.jobId,
        newHgncId,
        this.startIndex,
        this.computedPaginationOptions.size,
      );
    },
  },
  mounted() {
    this.startGetReferencesTimer();
    Bus.$on('clear-all', () => {
      clearTimeout(this.getReferencesTimerId);
      this.getReferences(
        this.jobId, this.hgncId, this.startIndex,
        this.computedPaginationOptions.size,
      );
    });
  },
  beforeDestroy() {
    clearTimeout(this.getReferencesTimerId);
  },
  data() {
    return {
      paginationOptions: {
        size: 10,
        page: 1,
      },
      symbol: '',
      referenceTotalCount: 0,
      references: [],
      getReferencesTimerId: '',
    };
  },
  computed: {
    startIndex() {
      return this.paginationOptions.size * (
        this.paginationOptions.page - 1);
    },
    computedPaginationOptions() {
      return {
        size: this.paginationOptions.size,
        page: this.paginationOptions.page,
        total: this.referenceTotalCount,
        label_: 'Rows',
        separator_: 'of',
        pageOptions_: [5, 10, 20, 50, 100, 200],  // constant
      };
    },
    translatedTitle() {
      return this.$t('result.reference.title', { symbol: this.symbol });
    },
  },
  methods: {
    startGetReferencesTimer() {
      console.log('Firing pull getReferences');  // eslint-disable-line no-console
      this.getReferences(
        this.jobId, this.hgncId, this.startIndex,
        this.computedPaginationOptions.size,
      );
      this.getReferencesTimerId = _.delay(
        this.startGetReferencesTimer, pullingConfig.timerMillis,
      );
    },
    getReferences(jobId, hgncId, startIndex, size) {
      if (_.isUndefined(jobId) || _.isUndefined(hgncId) ||
          _.isUndefined(startIndex) || _.isUndefined(size)) {
        return null;
      }
      return Promise.all([
        this.$http.get(`hgnc2symbols/${hgncId}`).promise,
        this.$http.get(`gene_pmid_counts/${jobId}/${hgncId}`).promise,
        this.$http.get(
          `gene_pmid_titles/${jobId}/${hgncId}/${startIndex}/${size}`).promise,
      ]).then(([symbolResponse, countResponse, titlesResponse]) => {
        const rawSymbol = symbolResponse.body;
        const rawCount = countResponse.body;
        const rawTitles = titlesResponse.body;
        this.symbol = _.get(rawSymbol, '[0].SYMBOL');
        this.referenceTotalCount = _.get(rawCount, '[0].COUNT(*)');
        this.references = _.map(rawTitles, rawTitle => ({
          pmid: _.get(rawTitle, 'PMID'),
          title: _.get(rawTitle, 'TITLE'),
        }));
      });
    },
    onPaginationPage(page) {
      _.assign(this.paginationOptions, { page });
      this.getReferences(
        this.jobId,
        this.hgncId,
        this.startIndex,
        this.computedPaginationOptions.size,
      );
    },
    onPaginationSize(size) {
      _.assign(this.paginationOptions, { page: 1, size });
      this.getReferences(
        this.jobId,
        this.hgncId,
        this.startIndex,
        this.computedPaginationOptions.size,
      );
    },
    onDownloadClicked() {
      this.$http.get(`gene_pmid_titles/${this.jobId}/${this.hgncId}`)
        .then((response) => {
          const pmidsJson = _.map(
            response.body, pmid => _.pick(pmid, ['PMID', 'TITLE']));
          return Papa.unparse(pmidsJson);
        })
        .then((pmidsJson) => {
          const blob = new Blob([pmidsJson]);
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = `${this.symbol}_references.csv`;
          link.click();
        });
    },
  },
});
</script>

<style scoped>
.result-reference {
  padding: 16px;
}

.result-reference-wrapper {
  width: 100%;
}

.a-tag-hover:hover {
  cursor: pointer;
}
</style>
