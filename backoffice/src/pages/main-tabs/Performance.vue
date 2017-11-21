<template>
  <div class="root">
    <div class="left-frame">
      <h1>Performance Test</h1>
      <md-whiteframe md-elevation="2" class="bcbTemp">
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
