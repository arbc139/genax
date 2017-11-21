<template>
<div class="root">
    <md-whiteframe class="root-paper" md-elevation="2">
      <div class="title-container">
        <h1>Welcome to GENAX</h1>
        <h4>GENAX uses the keywords you enter to dynamically find genes associated with your keywords.</h4>
        <span class="md-body-1">GENAX is a web-based sever which extracts gene-gene interactions from the biomedical literature. GENAX provides several customizing options which include time, cut-off, weight of edge and so on. Through dynamic collecting, GENAX always provides knowledge extracted from the latest publication. Furthermore, all analysis re-sults can be downloaded as csv file format.</span>
        <span class="md-body-1">All instruction needed to run GENAX is available <a href="http://help.genax.tools">here</a>.(or click right corner doucument button)</span>
        <span class="md-body-1">Below is the overall processing step of GENAX.</span>
      </div>
      <md-whiteframe class="chart-container" md-elevation="2">
        <img src="/static/GENAX_Step.png" style="height: 100%; width: 100%; background-size: contain;">
      </md-whiteframe>
    </md-whiteframe>
</div>

</template>

<script>
export default {
  name: 'about',
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
