<template>
  <div class="root">
    <md-whiteframe class="root-paper" md-elevation="2">
      <div class="title-container">
        <h1>Performance Test</h1>
        <span class="md-body-1">The performance of GENAX depends on the number of papers and the support cut off value.</span>
        <span class="md-body-1">The performance of GENAX is linearly proportional to the number of papers. Performance is also linearly proportional to the absolute value of log(support cut).</span>
      </div>
      <md-whiteframe class="chart-container" md-elevation="2">
        <div class="chart-instruction">
          <span class="md-title chart-title">Changing Number of the Papers</span>
          <span class="md-body-1">In order to investigate the effect of the number of papers on the performance of GENAX, we measured the time of the work by changing the time period of the paper about the same query and support cut. The search term is "Cancer" and the time period is 1 year, 2 years, ..., 10 years ago, from November 17, 2017. Support cut and other options are the default set provided by GENAX.</span>
          <span class="md-body-1">As the number of target papers increased, the working time increased linearly in proportion to this. The equation for the linear trend line of this data is as below</span>
          <span class="md-body-1">y = 0.000537x - 59.0 and R² is 0.991.</span>
          <span class="md-body-1">Sample data set test results with default options are like below table.</span>
          <div>
          <md-table>
            <md-table-row>
              <md-table-head>Query</md-table-head>
              <md-table-head>Time Period</md-table-head>
              <md-table-head>Number of Papers</md-table-head>
              <md-table-head>Time (s)</md-table-head>
            </md-table-row>

            <md-table-row>
              <md-table-cell>All PubMed Publication</md-table-cell>
              <md-table-cell>1900/01/01 ~ 2017/11/17</md-table-cell>
              <md-table-cell>27767389</md-table-cell>
              <md-table-cell>6999(&lt;2h)</md-table-cell>
            </md-table-row>

            <md-table-row>
              <md-table-cell>"Prostate Cancer"</md-table-cell>
              <md-table-cell>1900/01/01 ~ 2017/11/17</md-table-cell>
              <md-table-cell>149844</md-table-cell>
              <md-table-cell>31</md-table-cell>
            </md-table-row>

            <md-table-row>
              <md-table-cell>"Alzheimer's disease"</md-table-cell>
              <md-table-cell>1900/01/01 ~ 2017/11/17</md-table-cell>
              <md-table-cell>130017</md-table-cell>
              <md-table-cell>45</md-table-cell>
            </md-table-row>
          </md-table>
        </div>
        
        </div>
        <scatter-chart
          class="chart"
          :data="numberOfPaper.data"
          :options="numberOfPaper.options"
        />
      </md-whiteframe>
      <md-whiteframe class="chart-container" md-elevation="2">
        <div class="chart-instruction">
          <span class="md-title chart-title">Changing Support Cut</span>
          <span class="md-body-1">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</span>
        </div>
        <scatter-chart
          class="chart"
          :data="absoluteLog.data"
          :options="absoluteLog.options"
        />
      </md-whiteframe>
    </md-whiteframe>
  </div>
</template>

<script>
import ScatterChart from './ScatterChart';
import NumberOfPaperChartData from './NumberOfPaperChartData';
import AbsoluteLogChartData from './AbsoluteLogChartData';

export default {
  name: 'performance',
  components: { ScatterChart },
  data() {
    return {
      numberOfPaper: NumberOfPaperChartData,
      absoluteLog: AbsoluteLogChartData,
    };
  },
};
</script>

<style scoped>
.root {
  overflow: auto;
  padding: 16px;
}

.root-paper {
  display: flex;
  flex-direction: column;
  height: fit-content;
  padding: 16px;
}

.title-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

.chart-container {
  display: flex;
  flex-direction: row;
  padding: 16px;
  margin-bottom: 16px;
}

.chart-container:last-child {
  margin-bottom: 0;
}

.chart-instruction {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.chart-title {
  margin-bottom: 8px;
}

.chart {
  margin-left: 16px;
  flex: 1;
}
</style>
