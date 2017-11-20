<template>
  <div class="root">
    <div class="left-frame">
      <md-whiteframe md-elevation="2" class="bcbTemp">
        <h1>Performance Test</h1>
        <p1>The performance of GENAX depends on the number of papers and the support cut off value.</p1>
        <p1>The performance of GENAX is linearly proportional to the number of papers. Performance is also linearly proportional to the absolute value of log(support cut).</p1>
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
