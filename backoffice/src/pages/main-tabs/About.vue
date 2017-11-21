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
        <img src="/static/GENAX_Step.png" style="height: 80%; width: 80%; background-size: contain;">
      </md-whiteframe>
      <h4>Input</h4>
        <span class="md-body-1">GENAX makes query from user given keywords and time period. From the query, GENAX collects papers from PubMed.</span>
        <h4>Paper Collecting</h4>
        <span class="md-body-1">GENAX collects papers with multi-thread collecting. It allows dynamic paper collecting of GENAX. After all the target papers are collected, GENAX extracts MeSH terms from the papers. MeSH terms of the papers are converted to gene symbols with pre-defined rules.</span>
        <h4>Network Building</h4>
        <span class="md-body-1">From the paper-gene relationship, GENAX makes edges of the gene network. Genes that are simultaneously referenced in the same paper are the co-occurring genes. And Genes that appear alone in the papers are single-occurring genes. GENAX makes contingency tables for all co-occurring gene pair and calculate statistical significance of each co-occurring gene pair. All the gene pairs become edges of the gene network and statistical significance of the gene pair is the weight of the edge. GENAX makes another network by adding single occurring nodes to the co-occurring gene network.</span>
        <h4>Network Analyzing</h4>
        <span class="md-body-1">After network building ends, there are two networks. One is co-occurring genes only network, and the other is co-occurring genes plus single-occurring genes network. With those two networks, GENAX calculates centrality of each gene node. User can get the gene scores from centrality calculation. Also User can access the references where the genes are collected.</span>
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
