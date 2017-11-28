<template>
  <div class="root">
    <md-whiteframe class="root-paper" md-elevation="2">
      <div class="title-container">
        <h1>Performance Test</h1>
        <span class="md-body-1">The performance of GENAX depends on the number of papers and the support cut-off value.</span>
        <span class="md-body-1">The running time is liearly proportional to the absolute value of log<sub>10</sub>(minimum-support-cut) and the number of papers.</span>
      </div>
      <md-whiteframe class="chart-container" md-elevation="2">
        <div class="chart-instruction">
          <span class="md-title chart-title">Changing the Number of Papers</span>
          <span class="md-body-1">To evaluate the effect of the number of papers on the performance of GENAX, we measured the time of the work by changing the time period of the paper for the same query and support cut. The search term used in this case was "Cancer" and the time period was 1 year, 2 years, ..., 18 years ago, from November 17, 2017. Support cut and other options are the default set provided by GENAX.</span>
          <br>
          <span class="md-body-1">The running time increased linearly in proportion to the number of target papers. The equation for the linear trend line of these data is shown below.</span>
          <br>
          <span class="md-body-1">y = 0.000537x - 59.0 (R² = 0.991)</span>
          <br>
          <span class="md-body-1">The performance of the sample query with default options are given in the table below.</span>
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
              <md-table-cell>1900-01-01 ~ 2017-11-17</md-table-cell>
              <md-table-cell>27,767,389</md-table-cell>
              <md-table-cell>6,999 (&lt;2h)</md-table-cell>
            </md-table-row>

            <md-table-row>
              <md-table-cell>"Prostate cancer"</md-table-cell>
              <md-table-cell>1900-01-01 ~ 2017-11-17</md-table-cell>
              <md-table-cell>149,743</md-table-cell>
              <md-table-cell>35</md-table-cell>
            </md-table-row>

            <md-table-row>
              <md-table-cell>"Alzheimer's disease"</md-table-cell>
              <md-table-cell>1900-01-01 ~ 2017-11-17</md-table-cell>
              <md-table-cell>129,927</md-table-cell>
              <md-table-cell>30</md-table-cell>
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
          <span class="md-title chart-title">Changing the Support Cut</span>
          <span class="md-body-1">The support cut affects the running time of GENAX. The lower the support cut is, the longer it takes to get the result. We measured the time of the work by changing the support cut of the options. The search term was "Cancer" and the time period was from January 1, 1900 to November 17, 2017. Other options were set to default GENAX options.</span>
          <br>
          <span class="md-body-1">The running time of GENAX was linearly proprtional to |log<sub>10</sub>(minimum_support_cut)|</span>
          <span class="md-body-1">The equation for the linear trend line of these data was as below.</span>
          <br>
          <span class="md-body-1">y = 16.2 X + 1160 (R² = 0.948)</span>
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
