<template>
  <md-whiteframe md-elevation="2" class="result-table">
    <md-layout
      md-column
      md-align="start"
      md-vertical-align="center"
    >
      <md-layout
        class="button-container"
        md-row
        md-align="start"
      >
        <md-layout md-vertical-align="center">
          <md-button-toggle class="md-primary" md-single>
            <md-button
              :class="{ 'md-toggle': methodType === MethodType.coOccurence }"
              @click="onMethodClicked(MethodType.coOccurence)">
              {{ $t('result.table.methodType.coOccurence') }}
            </md-button>
            <md-button
              :class="{ 'md-toggle': methodType === MethodType.coOccurenceSingle }"
              @click="onMethodClicked(MethodType.coOccurenceSingle)">
              {{ $t('result.table.methodType.coOccurenceSingle') }}
            </md-button>
          </md-button-toggle>
        </md-layout>
        <md-layout md-align="end" md-flex>
          <md-menu
            md-direction="bottom left"
            :md-size="7"
          >
            <md-button class="md-raised" md-menu-trigger>
              {{ $t('common.downloadButton') }}
            </md-button>
            <md-menu-content>
              <md-menu-item @selected="onDownloadClick(1)">
                {{ $t('result.table.download.coOccurenceEdge') }}
              </md-menu-item>
              <md-menu-item @selected="onDownloadClick(2)">
                {{ $t('result.table.download.singleOccuringNode') }}
              </md-menu-item>
              <md-menu-item @selected="onDownloadClick(5)">
                {{ $t('result.table.download.geneScoresByCoOccurence') }}
              </md-menu-item>
              <md-menu-item @selected="onDownloadClick(6)">
                {{ $t('result.table.download.geneScoresByCoOccurenceNode') }}
              </md-menu-item>
            </md-menu-content>
          </md-menu>
        </md-layout>
      </md-layout>

      <md-table-card class="result-table-wrapper">
        <md-table
          :md-sort="sortOptions.field"
          :md-sort-type="sortOptions.type" @sort="onSort"
        >
          <md-table-header>
            <md-table-row>
              <md-table-head md-sort-by="symbol">Symbol</md-table-head>
              <md-table-head md-sort-by="hgncId">HGNC ID</md-table-head>
              <md-table-head md-sort-by="degree" md-numeric>
                Degree
              </md-table-head>
              <md-table-head md-sort-by="betweenness" md-numeric>
                Betweenness
              </md-table-head>
              <md-table-head md-sort-by="closeness" md-numeric>
                Closeness
              </md-table-head>
              <md-table-head md-sort-by="katz" md-numeric>
                Katz
              </md-table-head>
            </md-table-row>
          </md-table-header>

          <md-table-body>
            <md-table-row
              v-for="row in indexedPagedScores" :key="row.hgncId" :md-item="row"
            >
              <md-table-cell>
                <a class="a-tag-hover" @click="() => onSymbolClick(row.hgncId)">
                  {{ row.symbol }}
                </a>
              </md-table-cell>
              <md-table-cell>
                <a
                  target="_blank"
                  class="a-tag-hover"
                  :href="`https://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:${row.hgncId}`"
                >
                  {{ row.hgncId }}
                </a>
              </md-table-cell>
              <md-table-cell class="genax-numeric">{{ row.degree }}</md-table-cell>
              <md-table-cell class="genax-numeric">{{ row.betweenness }}</md-table-cell>
              <md-table-cell class="genax-numeric">{{ row.closeness }}</md-table-cell>
              <md-table-cell class="genax-numeric">{{ row.katz }}</md-table-cell>
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

import Bus from '../../components/Bus';
import MethodType from '../../structures/ResultTableMethodType';

import pullingConfig from '../../configs/pulling';

function convertMethodTypeToNetId(methodType) {
  switch (methodType) {
    case MethodType.coOccurence:
      return 3;
    case MethodType.coOccurenceSingle:
      return 4;
    default:
      return -1;
  }
}

export default Vue.component('result-table', {
  props: ['jobKey', 'jobId', 'onSymbolClick'],
  watch: {
    jobId(newJobId) {
      const netId = convertMethodTypeToNetId(this.methodType);
      this.getGeneScores(newJobId, netId);
    },
  },
  mounted() {
    this.startGetGeneScoresTimer();
    Bus.$on('clear-all', () => {
      clearTimeout(this.getGeneScoresTimerId);
      const netId = convertMethodTypeToNetId(this.methodType);
      this.getGeneScores(this.jobId, netId);
    });
  },
  beforeDestroy() {
    clearTimeout(this.getGeneScoresTimerId);
  },
  data() {
    return {
      methodType: MethodType.coOccurence,
      paginationOptions: {
        size: 10,
        page: 1,
      },
      sortOptions: {
        field: 'degree',
        type: 'desc',
      },
      // TODO(totoro): Saga에서 row 개수를 확인한 뒤, 일정 이상 사이즈가 크면,
      // pagination에서 lazy ajax request를 호출할 수 있어야 함.
      geneScores: [],
      getGeneScoresTimerId: '',
    };
  },
  computed: {
    // Inject
    MethodType() {
      return MethodType;
    },
    pagedScores() {
      return _.chain(this.geneScores)
        .orderBy(this.sortOptions.field, this.sortOptions.type)
        .chunk(this.paginationOptions.size)
        .value();
    },
    indexedPagedScores() {
      return this.pagedScores[this.paginationOptions.page - 1];
    },
    computedPaginationOptions() {
      return {
        size: this.paginationOptions.size,
        page: this.paginationOptions.page,
        total: _.flatten(this.pagedScores).length,
        label_: 'Rows',
        separator_: 'of',
        pageOptions_: [5, 10, 20, 50, 100, 200],  // constant
      };
    },
  },
  methods: {
    startGetGeneScoresTimer() {
      console.log('Firing pull getGeneScores');  // eslint-disable-line no-console
      const netId = convertMethodTypeToNetId(this.methodType);
      this.getGeneScores(this.jobId, netId);
      this.getGeneScoresTimerId = _.delay(
        this.startGetGeneScoresTimer, pullingConfig.timerMillis);
    },
    getGeneScores(jobId, netId) {
      if (_.isUndefined(jobId) || _.isUndefined(netId)) return;
      this.$http.get(`gene_scores/${jobId}/${netId}`)
        .then((response) => {
          const rawGeneScores = response.body;
          this.geneScores = _.map(rawGeneScores, geneScore => ({
            jobId: geneScore.J_ID,
            netId: geneScore.NET_ID,
            hgncId: geneScore.HGNC_ID,
            symbol: geneScore.SYMBOL,
            degree: _.ceil(geneScore.Degree, 6),
            betweenness: _.ceil(geneScore.Betweenness, 6),
            closeness: _.ceil(geneScore.Closeness, 6),
            clusteringCoef: _.ceil(geneScore.ClusteringCoef, 6),
            eigenVector: _.ceil(geneScore.Eigenvector, 6),
            katz: _.ceil(geneScore.Katz, 6),
          }));
        });
    },
    onMethodClicked(methodType) {
      this.methodType = methodType;
      const netId = convertMethodTypeToNetId(methodType);
      this.getGeneScores(this.jobId, netId);
    },
    onSort({ name, type }) {
      _.assign(this.sortOptions, { field: name, type });
    },
    onPaginationPage(page) {
      _.assign(this.paginationOptions, { page });
    },
    onPaginationSize(size) {
      _.assign(this.paginationOptions, { page: 1, size });
    },
    onDownloadClick(type) {
      if (_.isUndefined(this.jobId) || _.isUndefined(this.jobKey)) return;
      this.$http.get(`downloader/${this.jobId}/${this.jobKey}/${type}`)
        .then((response) => {
          const blob = new Blob(
            [response.data],
            { type: response.headers.map['content-type'] },
          );
          const link = document.createElement('a');
          link.href = window.URL.createObjectURL(blob);
          link.download = `${this.jobKey}_${this.toFileName(type)}.csv`;
          link.click();
        });
    },
    toFileName(downloadType) {
      switch (downloadType) {
        case 1: return 'edgeCooc';
        case 2: return 'SingleOccurringNode';
        case 5: return 'GeneCoOccurence';
        case 6: return 'GeneCoOccurenceSingleNode';
        default: return 'Error';
      }
    },
  },
});
</script>

<style scoped>
.button-container {
  width: 100%;
  margin-bottom: 8px;
}

.result-table {
  padding: 16px;
}

.result-table-wrapper {
  width: 100%;
}

.a-tag-hover:hover {
  cursor: pointer;
}

.genax-numeric {
  text-align: right;
}
</style>
