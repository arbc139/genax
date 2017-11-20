<template>
  <div class="root">
    <md-whiteframe md-whiteframe md-elevation="2" class="bcbTemp">
      <h1>Performance Test</h1>
        <p1>The performance of GENAX depends on the number of papers and the support cut off value.</p1>
        <p1>The performance of GENAX is linearly proportional to the number of papers. Performance is also linearly proportional to the absolute value of log(support cut).</p1>
      <div class="left-frame">
        <md-whiteframe md-elevation="2">
          <p1>In order to investigate the effect of the number of papers on the performance of GENAX, we measured the time of the work by changing the time period of the paper about the same query and support cut.</p1>
          <p1>The search term is "Cancer" and the time period is 1 year, 2 years, ..., 10 years ago, from November 17, 2017. Support cut and other options are the default set provided by GENAX.</p1>
          <p1>As the number of target papers increased, the working time increased linearly in proportion to this. The equation for the linear watershed of this data is</p1>
          <p1>y = 0.000537x - 59.0 and R² is 0.991</p>
            

          <scatter-chart
            :data="numberOfPaper.data"
            :option="numberOfPaper.option"
          />
        </md-whiteframe>
        <md-whiteframe md-elevation="2">
          <scatter-chart
            :data="absoluteLog.data"
            :option="absoluteLog.option"
          />
        </md-whiteframe>
    </md-whiteframe>
    </div>
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
  display: flex;
  flex-direction: row;
  overflow: auto;
}

.left-frame {
  display: flex;
  flex-direction: column;
  width: 50%;
  height: fit-content;
  padding: 16px;
}

.left-frame .md-whiteframe {
  margin-bottom: 16px;
}

.left-frame .md-whiteframe:last-child {
  margin-bottom: 0;
}

.bcbTemp {
  margin: 15px;
  padding: 15px;
}
</style>
